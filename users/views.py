from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer
from users.serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticatedOrReadOnly()]


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Пользователь успешно зарегистрирован",
                "user": serializer.data
            })
        return Response(serializer.errors)
