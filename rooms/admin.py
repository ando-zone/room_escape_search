from django.contrib import admin
from django.db.models import Count
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
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(review_count=Count('reviews'))
        return queryset

    Room.total_reviews.short_description = 'Total Reviews'
    Room.total_reviews.admin_order_field = 'review_count'

    actions = (reset_prices,)

    list_display = [
        "name",
        "branch",
        "genre",
        "total_reviews",
        "average_rating",
        "difficulty",
        "time_duration",
    ]
    list_filter = [
        "name",
        "genre",
        "difficulty",
        "time_duration",
    ]
    search_fields = ["name__startswith"]
