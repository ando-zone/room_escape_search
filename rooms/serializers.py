from rest_framework.serializers import ModelSerializer
from .models import Room
from brands.serializers import BrandSerializer

class RoomDetailSerializer(ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Room
        fields = "__all__"


class RoomSerializer(ModelSerializer):
    # TODO@Ando: brand를 여기서 보여주어야 하나 의문... (location이랑 겹침)
    # 애초에 brand 자체가 필요한지도 더 고민해보기. brand 별 review를 달 수는 있음.
    brand = BrandSerializer()

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
        )
        # depth = 1
