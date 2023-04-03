from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name
