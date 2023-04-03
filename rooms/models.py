from django.db import models
from common.models import CommonModel

# from reviews.models import Review


# Create your models here.
class Room(CommonModel):
    """Model Definition for Rooms"""

    class DifficultyChoices(models.IntegerChoices):
        ONE = (1, "🔑")  # (value, label) 괄호는 필수가 아님.
        TWO = (2, "🔑🔑")  # (value, label) 괄호는 필수가 아님.
        THREE = (3, "🔑🔑🔑")  # (value, label) 괄호는 필수가 아님.
        FOUR = (4, "🔑🔑🔑🔑")  # (value, label) 괄호는 필수가 아님.
        FIVE = (5, "🔑🔑🔑🔑🔑")  # (value, label) 괄호는 필수가 아님.

    # TODO@Ando: Description 추가해야 함.

    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField(help_text="Positive Numbers Only")
    # TODO@Ando: 이미지는 우선 room 한정해서 하나만 필요할 것 같아 일단은 photos app은 만들지 않기로 함.
    image = models.URLField(null=True, blank=True, max_length=1000)
    # TODO@Ando: airbnb에서는 category를 따로 하나의 앱으로 분류했음. 여기서는 필요하지 않을 것 같음.
    genre = models.CharField(max_length=140, null=True, blank=True)
    # 공식 난이도 (TODO@Ando: 체감 난이도는 유저가 직접 리뷰를 통해 달 수 있음)
    difficulty = models.PositiveIntegerField(
        choices=DifficultyChoices.choices,
    )
    fear_degree = models.PositiveIntegerField(
        choices=DifficultyChoices.choices, null=True, blank=True
    )
    activity = models.PositiveIntegerField(
        choices=DifficultyChoices.choices, null=True, blank=True
    )
    duration_of_time = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=140)
    brand = models.ForeignKey(
        "brands.Brand",
        on_delete=models.CASCADE,
    )

    # 아래 메서드에서 self를 꼭 self라고 쓰지 않아도 됩니다. room으로 바꿔도 아무런 지장이 없어요.
    def __str__(self) -> str:
        return self.name

    # TODO@Ando: total_reviews는 어떻게 보여줄 수 있을까? reverse accessors!
    # TODO@Ando: total_reviews를 이용하여 list_filter를 하는 방법은 없을까?
    def total_reviews(self) -> int:
        return self.reviews.count()

    def rating(room):
        count = room.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            # for review in room.reviews.all()로 적는 것보다 아래가 더 효율적임. (더 최적화 되어 있음.)
            for review in room.reviews.all().values("rating"):  # 반환값이 딕셔너리임.
                total_rating += review["rating"]
            return round(total_rating / count, 2)
