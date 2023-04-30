from django.db import models
from common.models import CommonModel

# from reviews.models import Review


# Create your models here.
class Room(CommonModel):
    """Model Definition for Rooms"""

    class DegreeChoices(models.IntegerChoices):
        ONE = (1, "🔑")  # (value, label) 괄호는 필수가 아님.
        TWO = (2, "🔑🔑")
        THREE = (3, "🔑🔑🔑")
        FOUR = (4, "🔑🔑🔑🔑")
        FIVE = (5, "🔑🔑🔑🔑🔑")

    name = models.CharField(max_length=140)
    genre = models.CharField(max_length=140, null=True, blank=True)
    difficulty = models.PositiveIntegerField(
        choices=DegreeChoices.choices, null=True, blank=True
    )
    fear_degree = models.PositiveIntegerField(
        choices=DegreeChoices.choices, null=True, blank=True
    )
    activity = models.PositiveIntegerField(
        choices=DegreeChoices.choices, null=True, blank=True
    )
    recommended_numb = models.PositiveIntegerField(null=True, blank=True)
    time_duration = models.PositiveIntegerField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True, max_length=1000)
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
    )

    # 아래 메서드에서 self를 꼭 self라고 쓰지 않아도 됩니다. room으로 바꿔도 아무런 지장이 없어요.
    def __str__(self) -> str:
        return self.name

    # TODO@Ando: total_reviews는 어떻게 보여줄 수 있을까? 정답은 reverse accessors!
    def total_reviews(self) -> int:
        return self.reviews.count()

    def average_rating(room):
        count = room.reviews.count()
        if count == 0:
            return 0

        total_rating = 0
        # for review in room.reviews.all()로 적는 것보다 아래가 더 효율적임. (더 최적화 되어 있음.)
        for review in room.reviews.all().values("rating"):  # 반환값이 딕셔너리임.
            total_rating += review["rating"]

        return round(total_rating / count, 2)

    def average_interior_score(room):
        count = room.reviews.count()
        if count == 0:
            return 0

        total_rating = 0
        for review in room.reviews.all().values("interior_score"):
            total_rating += review["interior_score"]

        return round(total_rating / count, 2)

    def average_story_score(room):
        count = room.reviews.count()
        if count == 0:
            return 0

        total_rating = 0
        for review in room.reviews.all().values("story_score"):
            total_rating += review["story_score"]

        return round(total_rating / count, 2)

    def average_creativity_score(room):
        count = room.reviews.count()
        if count == 0:
            return 0

        total_rating = 0
        for review in room.reviews.all().values("creativity_score"):
            total_rating += review["creativity_score"]

        return round(total_rating / count, 2)

    def average_problem_score(room):
        count = room.reviews.count()
        if count == 0:
            return 0

        total_rating = 0
        for review in room.reviews.all().values("problem_score"):
            total_rating += review["problem_score"]

        return round(total_rating / count, 2)

    def average_equipment_score(room):
        count = room.reviews.count()
        if count == 0:
            return 0

        total_rating = 0
        for review in room.reviews.all().values("equipment_score"):
            total_rating += review["equipment_score"]

        return round(total_rating / count, 2)
