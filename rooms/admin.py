from django.contrib import admin
from .models import Room
# Register your models here.


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
        "location",
        "brand",
        "genre",
        "total_reviews",
        "rating",
        "difficulty",
        "duration_of_time",
    ]
    list_filter = [
        "name",
        "price",
        "location",
        "genre",
        "difficulty",
        "duration_of_time",
    ]
    search_fields = [
        "name__startswith",
        "location"
    ]