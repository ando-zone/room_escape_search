from rest_framework import serializers
from .models import Room
from brands.serializers import BrandSerializer


class RoomDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()


class RoomListSerializer(serializers.ModelSerializer):
    # TODO@Ando: brand를 여기서 보여주어야 하나 의문... (location이랑 겹침)
    # 애초에 brand 자체가 필요한지도 더 고민해보기. brand 별 review를 달 수는 있음.
    brand = BrandSerializer()
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
            "location",
            "brand",
            "rating"
        )
        # depth = 1

    def get_rating(self, room):
        return room.rating()
