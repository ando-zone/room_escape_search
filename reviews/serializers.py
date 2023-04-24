from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "rating",
            "interior_score",
            "story_score",
            "creativity_score",
            "problem_score",
            "equipment_score",
        )