from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.permissions import IsAdmin, IsUser
from users.serializers import CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet для работы с пользователями. """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """ Возвращает serializer для действия. """
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """ Сохраняет нового пользователя. """
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        if user.role in ['admin', 'teacher']:
            user.is_staff = True
        user.save()

    def get_permissions(self):
        """ Разрешения для разных действий. """
        if self.request.user.is_anonymous and self.action != 'create':
            raise PermissionDenied("У вас нет доступа к этому ресурсу.")

        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'destroy', 'retrieve', 'update', 'partial_update']:
            return [IsAdmin()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsUser()]
        return [IsAuthenticated()]


class CustomTokenObtainPairView(TokenObtainPairView):
    """ Кастомный View для получения JWT токенов. """
    serializer_class = CustomTokenObtainPairSerializer
