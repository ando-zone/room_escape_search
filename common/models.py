from django.db import models

# Create your models here.

class CommonModel(models.Model):

    """Common Model Definition"""
    # 장고는 model이 abstract면 데이터베이스에 해당 모델을 추가하지 않음.
    # 이걸 class Meta를 이용해 표현 가능.
    # User를 제외한 모든 모델은 이것을 상속할 예정임.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True