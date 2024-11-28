from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'groups')
        read_only_fields = ('groups',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Попробуем найти пользователя по email
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
