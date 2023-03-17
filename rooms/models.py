from django.db import models
from common.models import CommonModel

# Create your models here.
class Room(CommonModel):
    """Model Definition for Rooms"""
    class DifficultyChoices(models.IntegerChoices):
        ONE = (1, "One") # (value, label) 괄호는 필수가 아님.
        TWO = (2, "Two") # (value, label) 괄호는 필수가 아님.
        THREE = (3, "Three") # (value, label) 괄호는 필수가 아님.
        FOUR = (4, "Four") # (value, label) 괄호는 필수가 아님.
        FIVE = (5, "Five") # (value, label) 괄호는 필수가 아님.

    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField(
        help_text="Positive Numbers Only"
    )
    image = models.ImageField(null=True, blank=True)
    # TODO@Ando: airbnb에서는 category를 따로 하나의 앱으로 분류했음. 여기서는 필요하지 않을 것 같음.
    genre = models.CharField(max_length=140, null=True, blank=True)
    # 공식 난이도 (TODO@Ando: 체감 난이도는 유저가 직접 리뷰를 통해 달 수 있음)
    difficulty = models.PositiveIntegerField(
        choices=DifficultyChoices.choices,
    )
    duration_of_time = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=140)
    brand = models.ForeignKey(
        "brands.Brand",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name

