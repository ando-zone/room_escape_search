from django.db import models

# Create your models here.
class Room(models.Model):
    """Model Definition for Rooms"""

    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField(
        help_text="Positive Numbers Only"
    )
    description = models.TextField()
    location = models.CharField(max_length=140)
    # brand = models.ForeignKey(
    #     "brands.Brand",
    #     on_delete=models.CASCADE,
    # )

    def __str__(self):
        return self.name

