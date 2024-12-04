from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, ModuleViewSet, LessonViewSet, EnrollmentAPIView

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('courses', CourseViewSet)
router.register('modules', ModuleViewSet)
router.register('lessons', LessonViewSet)

urlpatterns = [
    path('enrollment/', EnrollmentAPIView.as_view(), name='enrollment'),
              ] + router.urls
