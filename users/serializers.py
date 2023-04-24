from rest_framework.serializers import ModelSerializer
from .models import User


class TinyUserSerializer(ModelSerializer):
    """TinyUserSerializer

    Note:
        Review에서 작성자 정보를 대략적으로 알기 위해서 사용.
    """
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        # TODO@Ando: 아래를 보시면 filter가 아니라 exclude 입니다!
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
        read_only_fields = (
            "last_login",
            "date_joined",
            "is_admin",
        )