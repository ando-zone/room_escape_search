from rest_framework import serializers
from .models import Brand
from branches.models import Branch
from branches import serializers as branch_serializers


class BrandSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = (
            "pk",
            "name",
            "description",
            "average_rating"
        )

    def get_average_rating(self, brand):
        branches = Branch.objects.filter(brand=brand)
        total_rating = 0
        total_branches = 0

        branch_serializer_obj = branch_serializers.BranchSerializer()

        for branch in branches:
            branch_rating = branch_serializer_obj.get_average_rating(branch)
            # 평점이 한 번도 매겨지지 않았으면 해당 브랜치는 제외
            if not branch_rating:
                continue
            
            total_rating += branch_rating
            total_branches += 1

        return total_rating / total_branches if total_branches else 0