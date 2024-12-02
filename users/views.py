from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from users.permissions import IsAdmin, IsUser

from users.serializers import CustomTokenObtainPairSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def perform_create(self, serializer):

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    # def perform_update(self, serializer):
    #     user = serializer.save()
    #     if user.groups.filter(name='Teacher').exists() or user.groups.filter(name='Admin').exists():
    #         user.is_staff = True
    #         user.save()

    def get_permissions(self):
        """ Разрешения для разных действий """
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'destroy', 'retrieve', 'update', 'partial_update']:
            return [IsAdmin()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsUser()]
        return [IsAuthenticated()]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
