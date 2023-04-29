from rest_framework import status
from rest_framework.test import APITestCase
from .models import Brand
from .serializers import BrandSerializer
from branches.models import Branch
from branches.serializers import BranchSerializer
from reviews.models import Review
from rooms.models import Room

class BrandsAPITest(APITestCase):
    def setUp(self):
        self.brand1 = Brand.objects.create(
            name="Brand 1", description="Description 1"
        )
        self.brand2 = Brand.objects.create(
            name="Brand 2", description="Description 2"
        )
        self.brand3 = Brand.objects.create(
            name="Brand 3", description="Description 3"
        )

    def test_get_all_brands(self):
        url = "/api/v1/brands/"
        response = self.client.get(url)
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        self.assertEqual(response.data[0], serializer.data[0])
        self.assertEqual(response.data[1], serializer.data[1])
        self.assertEqual(response.data[2], serializer.data[2])


class BrandSerializerTestCase(APITestCase):
    def test_get_average_rating(self):
        brand = Brand.objects.create(name="Brand A")
        branch_1 = Branch.objects.create(
            name="Branch 1", address="Address 1", brand=brand
        )
        branch_2 = Branch.objects.create(
            name="Branch 2", address="Address 2", brand=brand
        )
        # 한 번도 평점이 매겨지지 않은 branch
        branch_3 = Branch.objects.create(
            name="Branch 2", address="Address 2", brand=brand
        )
        room1 = Room.objects.create(
            name="Room 1",
            branch=branch_1,
            price="10000",
            difficulty=1,
        )
        room2 = Room.objects.create(
            name="Room 2",
            branch=branch_1,
            price="10000",
            difficulty=1,
        )
        room3 = Room.objects.create(
            name="Room 3",
            branch=branch_2,
            price="10000",
            difficulty=1,
        )

        # Create some reviews for rooms
        Review.objects.create(
            room=room1,
            rating=4,
            interior_score=1,
            story_score=1,
            creativity_score=1,
            problem_score=1,
            equipment_score=1,
        )
        Review.objects.create(
            room=room2,
            rating=4,
            interior_score=1,
            story_score=1,
            creativity_score=1,
            problem_score=1,
            equipment_score=1,
        )
        Review.objects.create(
            room=room3,
            rating=5,
            interior_score=1,
            story_score=1,
            creativity_score=1,
            problem_score=1,
            equipment_score=1,
        )

        serializer = BrandSerializer(brand)

        self.assertEqual(serializer.data["average_rating"], 4.5)