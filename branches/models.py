from django.db import models

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    booking_link = models.CharField(max_length=1000, null=True, blank=True)
    brand = models.ForeignKey(
        "brands.Brand",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self) -> str:
        return self.name
