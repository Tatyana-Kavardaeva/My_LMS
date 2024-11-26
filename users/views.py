from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer
from rest_framework.permissions import AllowAny


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticatedOrReadOnly()]
