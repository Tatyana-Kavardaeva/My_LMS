from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from users.validators import AdminRequiredValidator


class UserSerializer(serializers.ModelSerializer):
    """ Serializer, используемый для отображения информации о пользователе. """

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'phone', 'avatar')
        read_only_fields = ('role',)


class RegisterSerializer(serializers.ModelSerializer):
    """ Serializer для регистрации пользователя. """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'role')
        validators = [AdminRequiredValidator('role')]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомизированный serializer для получения пары токенов JWT (access и refresh) с дополнительной валидацией.
    """

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль.")
        if not user.is_active:
            raise serializers.ValidationError("Пользователь не активен.")

        # Возвращаем стандартные токены
        data = super().validate(attrs)
        return data
