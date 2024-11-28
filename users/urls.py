from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import UserViewSet, CustomTokenObtainPairView

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [

    path('login/', CustomTokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token-refresh'),

] + router.urls
