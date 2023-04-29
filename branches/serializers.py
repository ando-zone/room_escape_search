from rest_framework import serializers
from .models import Branch
from brands.serializers import BrandSerializer
from rooms.models import Room

class BranchSerializer(serializers.ModelSerializer):

    brand = BrandSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = (
            "pk",
            "name",
            "address",
            "brand",
            "average_rating"
        )

    def get_average_rating(self, branch):
        rooms = Room.objects.filter(branch=branch)
        total_rating = 0
        total_rooms = 0

        for room in rooms:
            room_rating = room.average_rating()
            # 평점이 한 번도 매겨지지 않았으면 해당 방은 제외
            if not room_rating:
                continue

            total_rating += room.average_rating()
            total_rooms += 1

        return round(total_rating / total_rooms,2) if total_rooms else 0