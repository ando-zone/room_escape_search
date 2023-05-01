from django.http import HttpRequest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from .models import Room
from .serializers import RoomListSerializer, RoomDetailSerializer
from branches.models import Branch
from brands.models import Brand
from users.models import User


class RoomsAPITest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("123")
        user.save()
        self.user = user
        self.brand = Brand.objects.create(name="test_brand")
        self.branch = Branch.objects.create(
            name="test_branch", brand=self.brand
        )
        self.room = Room.objects.create(name="test_room", branch=self.branch)

    def test_get_rooms(self):
        url = "/api/v1/rooms/"
        response = self.client.get(url)
        rooms = Room.objects.all()
        serializer = RoomListSerializer(rooms, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_room(self):
        url = "/api/v1/rooms/"
        data = {"name": "test_room_B", "branch": self.branch.pk}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data=data)
        room = Room.objects.get(name="test_room_B")
        request = HttpRequest()
        request.user = self.user
        serializer = RoomDetailSerializer(room, context={"request": request})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)

    def test_create_room_without_branch(self):
        self.client.force_authenticate(user=self.user)

        url = "/api/v1/rooms/"
        data = {"name": "test_room_B"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "detail": ErrorDetail(
                    string="Branch is required.", code="parse_error"
                )
            },
        )

    def test_create_room_invalid_branch(self):
        self.client.force_authenticate(user=self.user)

        url = "/api/v1/rooms/"
        data = {"name": "test_room_B", "branch": -1}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "detail": ErrorDetail(
                    string="Branch not found.", code="parse_error"
                )
            },
        )
