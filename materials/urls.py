# from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, ModuleViewSet, LessonViewSet

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('courses', CourseViewSet)
router.register('modules', ModuleViewSet)
router.register('lessons', LessonViewSet)

urlpatterns = [

] + router.urls