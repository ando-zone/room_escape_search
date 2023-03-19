from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from .models import Room
from brands.models import Brand
from .serializers import RoomListSerializer, RoomDetailSerializer


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

            room = serializer.save(
                brand = brand
            )
            serializer = RoomDetailSerializer(room)
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
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
