from rest_framework import serializers
from .models import Room
from branches.serializers import BranchSerializer
from reviews.serializers import ReviewSerializer
from wishlists.models import Wishlist


class RoomDetailSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    # TODO@Ando: api/v1/rooms/1/reviews로 대체합니다.
    # reviews = ReviewSerializer(
    #     many=True,
    #     read_only=True,
    # )

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_liked(self, room):
        request = self.context["request"]
        if request.user.is_authenticated:
            return Wishlist.objects.filter(
                user=request.user,
                rooms__pk=room.pk,
            ).exists()
        return False

class RoomListSerializer(serializers.ModelSerializer):
    # TODO@Ando: brand를 여기서 보여주어야 하나 의문... (location이랑 겹침)
    # 애초에 brand 자체가 필요한지도 더 고민해보기. brand 별 review를 달 수는 있음.
    branch = BranchSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        # fields = "__all__"
        fields = (
            "pk",
            "name",
            "image",
            "genre",
            "difficulty",
            "duration_of_time",
            "branch",
            "rating",
        )
        # depth = 1

    def get_rating(self, room):
        return room.rating()
