from rest_framework import serializers
from .models import Room
from branches.serializers import BranchSerializer
from reviews.serializers import ReviewSerializer
from wishlists.models import Wishlist


class RoomDetailSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    average_interior_score = serializers.SerializerMethodField()
    average_story_score = serializers.SerializerMethodField()
    average_creativity_score = serializers.SerializerMethodField()
    average_problem_score = serializers.SerializerMethodField()
    average_equipment_score = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_average_rating(self, room):
        return room.average_rating()

    def get_average_interior_score(self, room):
        return room.average_interior_score()

    def get_average_story_score(self, room):
        return room.average_story_score()

    def get_average_creativity_score(self, room):
        return room.average_creativity_score()

    def get_average_problem_score(self, room):
        return room.average_problem_score()

    def get_average_equipment_score(self, room):
        return room.average_equipment_score()

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
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        # fields = "__all__"
        fields = (
            "pk",
            "name",
            "image_url",
            "genre",
            "difficulty",
            "time_duration",
            "branch",
            "average_rating",
        )
        # depth = 1

    def get_average_rating(self, room):
        return room.average_rating()
