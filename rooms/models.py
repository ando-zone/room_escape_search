from django.db import models

# Create your models here.
class Room(models.Model):
    """Model Definition for Rooms"""
    class DifficultyChoices(models.IntegerChoices):
        ONE = (1, "One") # (value, label)
        TWO = (2, "Two") # (value, label)
        THREE = (3, "Three") # (value, label)
        FOUR = (4, "Four") # (value, label)
        FIVE = (5, "Five") # (value, label)

    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField(
        help_text="Positive Numbers Only"
    )
    image = models.ImageField(null=True, blank=True)
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

    def __str__(self):
        return self.name

