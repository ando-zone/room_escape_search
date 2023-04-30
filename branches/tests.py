from rest_framework import status
from rest_framework.test import APITestCase
from .models import Branch
from .serializers import BranchSerializer
from brands.models import Brand
from reviews.models import Review
from rooms.models import Room


class BranchesAPITest(APITestCase):
    def setUp(self):
        # Sample brands for testing
        self.brand1 = Brand.objects.create(
            name="Brand 1", description="Best Brand"
        )
        self.brand2 = Brand.objects.create(
            name="Brand 2", description="Good Brand"
        )

        # Sample branches for testing
        self.branch1 = Branch.objects.create(
            name="Branch 1", address="Address 1", brand=self.brand1
        )
        self.branch2 = Branch.objects.create(
            name="Branch 2", address="Address 2", brand=self.brand1
        )
        self.branch3 = Branch.objects.create(
            name="Branch 3", address="Address 3", brand=self.brand1
        )
        self.branch4 = Branch.objects.create(
            name="Branch 4", address="Address 4", brand=self.brand2
        )
        self.branch5 = Branch.objects.create(
            name="Branch 5", address="Address 5", brand=self.brand2
        )
        self.branch6 = Branch.objects.create(
            name="Branch 6", address="Address 6", brand=self.brand2
        )

    def test_get_branches(self):
        url = "/api/v1/branches/"
        response = self.client.get(url)
        branches = Branch.objects.all()[:3]
        serializer = BranchSerializer(branches, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_branches_pagination(self):
        url = "/api/v1/branches/?page=2"
        response = self.client.get(url)
        branches = Branch.objects.all()[3:6]
        serializer = BranchSerializer(branches, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_branches_invalid_page(self):
        url = "/api/v1/branches/?page=invalid"
        response = self.client.get(url)
        branches = Branch.objects.all()[:3]
        serializer = BranchSerializer(branches, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class BranchSerializerTestCase(APITestCase):
    def test_get_average_rating(self):
        brand = Brand.objects.create(name="Brand A")
        branch = Branch.objects.create(
            name="Branch 1", address="Address 1", brand=brand
        )
        room1 = Room.objects.create(
            name="Room 1",
            branch=branch,
            difficulty=1,
        )
        room2 = Room.objects.create(
            name="Room 2",
            branch=branch,
            difficulty=1,
        )
        # 한 번도 평점이 매겨지지 않은 room
        room3 = Room.objects.create(
            name="Room 3",
            branch=branch,
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
            room=room1,
            rating=3,
            interior_score=1,
            story_score=1,
            creativity_score=1,
            problem_score=1,
            equipment_score=1,
        )
        Review.objects.create(
            room=room2,
            rating=5,
            interior_score=1,
            story_score=1,
            creativity_score=1,
            problem_score=1,
            equipment_score=1,
        )

        serializer = BranchSerializer(branch)

        self.assertEqual(serializer.data["average_rating"], 4.25)
