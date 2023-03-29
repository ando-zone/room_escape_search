from django.urls import path
from . import views

urlpatterns = [
    path("", views.Brands.as_view()),
]