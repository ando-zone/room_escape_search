from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
