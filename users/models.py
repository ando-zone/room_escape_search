from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male") # (value, label)
        FEMALE = ("female", "Female") # (value, label)

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, default="")
    is_admin = models.BooleanField(default=False) #non-nullable field (True of False)
    avatar = models.ImageField()
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )