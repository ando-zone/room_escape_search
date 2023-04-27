from django.urls import path
from . import views

urlpatterns = [
    path("", views.Branches.as_view()),
]