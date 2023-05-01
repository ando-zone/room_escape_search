from rest_framework import serializers
from .models import Room
from branches.serializers import BranchSerializer
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
    branch = BranchSerializer()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
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

    def get_average_rating(self, room):
        return room.average_rating()
