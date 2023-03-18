from django.contrib import admin
from .models import Room
# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
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