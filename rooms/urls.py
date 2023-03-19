from django.urls import path
from . import views

urlpatterns = [
    path("", views.Rooms.as_view()),
]