from django.db import models
from common.models import CommonModel


# Create your models here.
class Review(CommonModel):
    class DifficultyChoices(models.IntegerChoices):
        ONE = (1, "⭐️") # (value, label) 괄호는 필수가 아님.
        TWO = (2, "⭐️⭐️") # (value, label) 괄호는 필수가 아님.
        THREE = (3, "⭐️⭐️⭐️") # (value, label) 괄호는 필수가 아님.
        FOUR = (4, "⭐️⭐️⭐️⭐️") # (value, label) 괄호는 필수가 아님.
        FIVE = (5, "⭐️⭐️⭐️⭐️⭐️") # (value, label) 괄호는 필수가 아님.

    user = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL
    )
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    payload = models.TextField()
    rating = models.PositiveIntegerField(
        choices=DifficultyChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐️"
