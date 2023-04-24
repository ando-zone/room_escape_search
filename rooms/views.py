from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Room
from branches.models import Branch
from .serializers import RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer


# Create your views here.
class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            branch_pk = request.data.get("branch")

            if not branch_pk:
                raise ParseError("Branch is required.")

            try:
                branch = Branch.objects.get(pk=branch_pk)
            except Branch.DoesNotExist:
                raise ParseError("Branch not found.")

            room = serializer.save(branch=branch)
            serializer = RoomDetailSerializer(
                room, context={"request": request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_room = serializer.save()
            return Response(
                RoomDetailSerializer(
                    updated_room, context={"request": request}
                ).data, status=HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        room = self.get_object(pk)
        room.delete()

        return Response({"ok": "방이 성공적으로 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)


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
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)

    # TODO@Ando: put과 delete는 여기가 아니라 reviews에서 구현해야 할 것 같다.
