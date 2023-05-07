from django.db import models
from common.models import CommonModel


def get_average_score_for_room(room: object, score_type: str) -> float:
    total_rating = 0
    count = 0
    # for review in room.reviews.all()로 적는 것보다 아래가 더 효율적임. (더 최적화 되어 있음.)
    for review in room.reviews.all().values(score_type):  # 반환값이 딕셔너리임.
        if review[score_type] is None:
            continue

        total_rating += review[score_type]
        count += 1

    if count == 0:
        return float(0)

    return round(total_rating / count, 2)


# Create your models here.
class Room(CommonModel):
    """Model Definition for Rooms"""

    class DegreeIntChoices(models.IntegerChoices):
        ONE = (1, "🔑")  # (value, label) 괄호는 필수가 아님.
        TWO = (2, "🔑🔑")
        THREE = (3, "🔑🔑🔑")
        FOUR = (4, "🔑🔑🔑🔑")
        FIVE = (5, "🔑🔑🔑🔑🔑")

    class ActivityDegreeChoices(models.TextChoices):
        LOW = ("낮음", "🔑")
        MIDDLE = ("중간", "🔑🔑")
        HIGH = ("높음", "🔑🔑🔑")

    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, null=True, blank=True)
    difficulty = models.PositiveIntegerField(
        choices=DegreeIntChoices.choices, null=True, blank=True
    )
    fear_degree = models.PositiveIntegerField(
        choices=DegreeIntChoices.choices, null=True, blank=True
    )
    activity = models.TextField(
        choices=ActivityDegreeChoices.choices, null=True, blank=True
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
        return get_average_score_for_room(room, "rating")

    def average_interior_score(room):
        return get_average_score_for_room(room, "interior_score")

    def average_story_score(room):
        return get_average_score_for_room(room, "story_score")

    def average_creativity_score(room):
        return get_average_score_for_room(room, "creativity_score")

    def average_problem_score(room):
        return get_average_score_for_room(room, "problem_score")

    def average_equipment_score(room):
        return get_average_score_for_room(room, "equipment_score")
