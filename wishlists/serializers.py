from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomListSerializer
from .models import Wishlist


class WishlistListSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
        )


class WishlistDetailSerializer(ModelSerializer):

    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )