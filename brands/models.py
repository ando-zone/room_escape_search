from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    # TODO@Ando: 해당하는 지점을 연결해야 함.

    def __str__(self) -> str:
        return self.name
