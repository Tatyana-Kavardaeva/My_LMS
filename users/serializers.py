from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'groups', 'user_permissions', 'is_active', 'is_staff', 'is_superuser')

