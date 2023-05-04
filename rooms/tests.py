from django.http import HttpRequest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from .models import Room
from .serializers import RoomListSerializer, RoomDetailSerializer
from branches.models import Branch
from brands.models import Brand
from reviews.models import Review
from reviews.serializers import ReviewSerializer
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

    def test_get_room_detail(self):
        url = f"/api/v1/rooms/{self.room.pk}"
        response = self.client.get(url)
        request = HttpRequest()
        request.user = self.user
        serializer = RoomDetailSerializer(
            self.room, context={"request": request}
        )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_room(self):
        self.client.force_authenticate(user=self.user)

        url = f"/api/v1/rooms/{self.room.pk}"
        data = {"name": "updated_room_name"}
        response = self.client.put(url, data=data)
        updated_room = Room.objects.get(pk=self.room.pk)
        request = HttpRequest()
        request.user = self.user
        serializer = RoomDetailSerializer(
            updated_room, context={"request": request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(updated_room.name, data["name"])

    def test_update_room_invalid_data(self):
        self.client.force_authenticate(user=self.user)

        url = f"/api/v1/rooms/{self.room.pk}"
        data = {"name": ""}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_delete_room(self):
        self.client.force_authenticate(user=self.user)

        url = f"/api/v1/rooms/{self.room.pk}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(Room.DoesNotExist, Room.objects.get, pk=self.room.pk)

    def test_get_room_reviews(self):
        # Create reviews for testing
        for numb in range(5):
            Review.objects.create(
                user=User.objects.create(
                    username=f"test_{numb}", email=f"test_{numb}@gmail.com"
                ),
                room=self.room,
                rating=Review.ScoreChoices.FIVE,
            )

        for page_numb in [1, 2]:
            url = f"/api/v1/rooms/{self.room.pk}/reviews?page={page_numb}"
            response = self.client.get(url)
            page_size = 3
            reviews = self.room.reviews.all()[
                page_size * (page_numb - 1) : page_size * page_numb
            ]
            serializer = ReviewSerializer(reviews, many=True)
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_room_review(self):
        self.client.force_authenticate(user=self.user)

        url = f"/api/v1/rooms/{self.room.pk}/reviews"
        data = {"rating": Review.ScoreChoices.FIVE}
        response = self.client.post(url, data=data)
        review = Review.objects.get(user=self.user, room=self.room)
        serializer = ReviewSerializer(review)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_create_room_review_invalid_data(self):
        self.client.force_authenticate(user=self.user)

        url = f"/api/v1/rooms/{self.room.pk}/reviews"
        # Invalid rating value
        data = {"rating": 6}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)


class RoomFiltersAPITest(APITestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name="brand")
        self.branch1 = Branch.objects.create(
            name="branch1", city="서울특별시", district="성북구", brand=self.brand
        )
        self.branch2 = Branch.objects.create(
            name="branch2", city="서울특별시", district="종로구", brand=self.brand
        )
        self.user1 = User.objects.create(username=f"user1", email=f"user1_mail")
        self.user2 = User.objects.create(username=f"user2", email=f"user2_mail")

        self.room1 = Room.objects.create(
            name="room1",
            branch=self.branch1,
            time_duration=75,
            difficulty=5,
            fear_degree=1,  # TODO@Ando: 0도 값이될 수 있음.
            activity="높음",
            genre="SF/판타지",
        )
        Review.objects.create(
            user=self.user1, room=self.room1, rating=5, interior_score=5
        )
        Review.objects.create(
            user=self.user2, room=self.room1, rating=4, interior_score=4
        )

        self.room2 = Room.objects.create(
            name="room2",
            branch=self.branch2,
            time_duration=60,
            difficulty=4,
            fear_degree=3,
            activity="낮음",
            genre="멜로/로맨스",
        )
        Review.objects.create(
            user=self.user1, room=self.room2, rating=3, interior_score=3
        )
        Review.objects.create(
            user=self.user2, room=self.room2, rating=2, interior_score=2
        )

    def test_append_rooms_by_avg_score(self):
        url = f"/api/v1/rooms/filters"
        for score_type in ["rating", "interior_score"]:
            params = {
                f"min_avg_{score_type}": 3,
                f"max_avg_{score_type}": 5,
            }
            response = self.client.get(url, params)
            rooms = list()
            for room in Room.objects.all():
                if (
                    room.average_rating() >= params[f"min_avg_{score_type}"]
                    and room.average_rating() <= params[f"max_avg_{score_type}"]
                ):
                    rooms.append(room)
            room_obj = Room.objects.filter(pk__in=[room.pk for room in rooms])
            serializer = RoomListSerializer(room_obj, many=True)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)

    def test_append_rooms_by_time_duration(self):
        url = f"/api/v1/rooms/filters"
        params = {
            "min_time_duration": 60,
            "max_time_duration": 75,
        }
        response = self.client.get(url, params)
        rooms = list()
        for room in Room.objects.all():
            if (
                room.time_duration >= params["min_time_duration"]
                and room.time_duration <= params["max_time_duration"]
            ):
                rooms.append(room)
        room_obj = Room.objects.filter(pk__in=[room.pk for room in rooms])
        serializer = RoomListSerializer(room_obj, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_params_with_city(self):
        url = f"/api/v1/rooms/filters"
        params = {"city": "서울특별시,인천광역시"}
        response_1 = self.client.get(url, params)
        params = {"district": "서울특별시|인천광역시"}
        response_2 = self.client.get(url, params)
        rooms = list()
        for room in Room.objects.all():
            if room.branch.city in {"서울특별시", "인천광역시"}:
                rooms.append(room)
        room_obj = Room.objects.filter(pk__in=[room.pk for room in rooms])
        serializer = RoomListSerializer(room_obj, many=True)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_1.data, serializer.data)
        self.assertNotEqual(response_2.data, serializer.data)

    def test_get_params_with_district(self):
        url = f"/api/v1/rooms/filters"
        params = {"district": "종로구,성북구"}
        response_1 = self.client.get(url, params)
        params = {"district": "종로구|성북구"}
        response_2 = self.client.get(url, params)
        params = {"district": "종로구"}
        response_3 = self.client.get(url, params)
        rooms = list()
        for room in Room.objects.all():
            if room.branch.district in {"종로구", "성북구"}:
                rooms.append(room)
        room_obj = Room.objects.filter(pk__in=[room.pk for room in rooms])
        serializer = RoomListSerializer(room_obj, many=True)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_1.data, serializer.data)
        self.assertNotEqual(response_2.data, serializer.data)
        self.assertNotEqual(response_3.data, serializer.data)

    def test_get_params_with_difficulty(self):
        url = f"/api/v1/rooms/filters"

        params = {"difficulty": "1|2|3|4|5"}
        with self.assertRaises(ValueError):
            response = self.client.get(url, params)

        params = {"difficulty": "1,2,3,4,5"}
        response_1 = self.client.get(url, params)
        params = {"difficulty": "4,5"}
        response_2 = self.client.get(url, params)
        rooms = list()
        for room in Room.objects.all():
            if room.difficulty in {1, 2, 3, 4, 5}:
                rooms.append(room)
        room_obj = Room.objects.filter(pk__in=[room.pk for room in rooms])
        serializer = RoomListSerializer(room_obj, many=True)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_1.data, serializer.data)
        self.assertEqual(response_2.data, serializer.data)
