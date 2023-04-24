from django.contrib import admin
from .models import Room

# Register your models here.


# TODO@Ando: action만 따로 모아서 다른 모듈로 분리할 수 있음. 사용할 때는 이 곳에 import해야 함
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    # print(model_admin)
    # print(dir(request))
    # print(rooms)
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)

    list_display = [
        "name",
        "price",
        "branch",
        "genre",
        "total_reviews",
        "rating",
        "difficulty",
        "duration_of_time",
    ]
    list_filter = [
        "name",
        "price",
        "genre",
        "difficulty",
        "duration_of_time",
    ]
    search_fields = ["name__startswith"]
