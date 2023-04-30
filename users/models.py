from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male") # (value, label)
        FEMALE = ("female", "Female") # (value, label)

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    name = models.CharField(max_length=150, default="")
    is_admin = models.BooleanField(default=False) #non-nullable field (True of False)
    avatar = models.URLField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        blank=True,
        null=True
    )