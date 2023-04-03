from django.db import models

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=140)
    location = models.CharField(max_length=1000)
    brand = models.ForeignKey(
        "brands.Brand",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self) -> str:
        return self.name
