from django.db import models
from common.models import CommonModel


# Create your models here.
class Review(CommonModel):
    class DifficultyChoices(models.IntegerChoices):
        ONE = (1, "⭐️")  # (value, label) 괄호는 필수가 아님.
        TWO = (2, "⭐️⭐️")  # (value, label) 괄호는 필수가 아님.
        THREE = (3, "⭐️⭐️⭐️")  # (value, label) 괄호는 필수가 아님.
        FOUR = (4, "⭐️⭐️⭐️⭐️")  # (value, label) 괄호는 필수가 아님.
        FIVE = (5, "⭐️⭐️⭐️⭐️⭐️")  # (value, label) 괄호는 필수가 아님.

    # TODO@Ando: related_name을 통해서 reverse access 사용 시, _set으로 끝나는 것을 찾지 않아도 된다.
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviews",
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField(
        choices=DifficultyChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐️"
