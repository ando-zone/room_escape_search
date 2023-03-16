from django.contrib import admin
from .models import Room
# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "location",
    ]
    list_filter = [
        "name",
        "price",
        "location"
    ]
    search_fields = [
        "name__startswith",
        "location"
    ]