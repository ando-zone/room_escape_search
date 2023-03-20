from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Room
from brands.models import Brand
from .serializers import RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer


# Create your views here.
class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            brand_pk = request.data.get("brand")

            if not brand_pk:
                raise ParseError("Brand is required.")

            try:
                brand = Brand.objects.get(pk=brand_pk)
            except Brand.DoesNotExist:
                raise ParseError("Brand not found.")

            room = serializer.save(brand=brand)
            serializer = RoomDetailSerializer(
                room, context={"request": request}
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        selializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if selializer.is_valid():
            updated_room = selializer.save()
            return Response(
                RoomDetailSerializer(
                    updated_room, context={"request": request}
                ).data
            )
        else:
            return Response(selializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        room.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],  # 노션 노트 참조.
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)

    # TODO@Ando: put과 delete는 여기가 아니라 reviews에서 구현해야 할 것 같다.
