from unittest import mock

from rest_framework.test import APIClient, APITestCase
from branches.models import Branch
from brands.models import Brand
from rooms.models import Room
from users.models import User
from .models import Wishlist
from .serializers import WishlistListSerializer, WishlistDetailSerializer


class WishlistsAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )

        test_brand = Brand.objects.create(
            name="test_Brand", description="Best Brand"
        )
        test_branch = Branch.objects.create(
            name="tset_Branch", address="Address 1", brand=test_brand
        )
        test_room_A = Room.objects.create(
            name="test_room_A", difficulty=1, branch=test_branch
        )
        test_room_B = Room.objects.create(
            name="test_room_B", difficulty=1, branch=test_branch
        )
        self.wishlist = Wishlist.objects.create(
            name="test_wishlist_A",
            user=self.user,
        )
        self.wishlist.rooms.set([test_room_A, test_room_B])

    def test_get_wishlists(self):
        url = "/api/v1/wishlists/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        wishlist = Wishlist.objects.all()
        serializer = WishlistListSerializer(wishlist, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create_wishlist(self):
        url = "/api/v1/wishlists/"
        data = {"name": "test_wishlist_B", "user": self.user}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data=data)
        wishlist = Wishlist.objects.get(name="test_wishlist_B")
        serializer = WishlistListSerializer(wishlist)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)

    @mock.patch(
        "rest_framework.serializers.BaseSerializer.is_valid", return_value=False
    )
    @mock.patch(
        "rest_framework.serializers.BaseSerializer.errors",
        new_callable=mock.PropertyMock,
    )
    def test_create_wishlist_invalid_form(self, mock_errors, mock_is_valid):
        self.client.force_authenticate(user=self.user)

        url = f"/api/v1/wishlists/"
        data = {"name": "test_wishlist_B", "user": self.user}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 406)

    def test_get_wishlist_detail(self):
        pk_number = 1
        url = f"/api/v1/wishlists/{pk_number}"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        wishlist = Wishlist.objects.get(pk=pk_number)
        serializer = WishlistDetailSerializer(wishlist)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_delete_wishlist(self):
        pk_number = 1
        url = f"/api/v1/wishlists/{pk_number}"

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_update_wishlist(self):
        pk_number = 1
        url = f"/api/v1/wishlists/{pk_number}"
        data = {"name": "test_wishlist_AAA"}

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.user)

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "test_wishlist_AAA")

    @mock.patch(
        "rest_framework.serializers.BaseSerializer.is_valid", return_value=False
    )
    @mock.patch(
        "rest_framework.serializers.BaseSerializer.errors",
        new_callable=mock.PropertyMock,
    )
    def test_update_wishlist_invalid_form(self, mock_errors, mock_is_valid):
        self.client.force_authenticate(user=self.user)

        pk_number = 1
        url = f"/api/v1/wishlists/{pk_number}"
        data = {"name": "test_wishlist_AAA"}

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 406)

    def test_wishlist_toggle(self):
        self.client.force_authenticate(user=self.user)

        pk_wishlist_num = 1
        pk_room_num = 1

        # toggle_to_remove
        url = f"/api/v1/wishlists/{pk_wishlist_num}/rooms/{pk_room_num}"
        
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)

        wishlist = Wishlist.objects.get(pk=pk_wishlist_num)
        serializer = WishlistDetailSerializer(wishlist)
        self.assertEqual(len(serializer.data["rooms"]), 1)
        self.assertNotEqual(serializer.data["rooms"][0]["pk"], pk_room_num)

        # toggle_to_add
        url = f"/api/v1/wishlists/{pk_wishlist_num}/rooms/{pk_room_num}"
        
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)

        wishlist = Wishlist.objects.get(pk=pk_wishlist_num)
        serializer = WishlistDetailSerializer(wishlist)
        self.assertEqual(len(serializer.data["rooms"]), 2)
        self.assertEqual(serializer.data["rooms"][0]["pk"], pk_room_num)
