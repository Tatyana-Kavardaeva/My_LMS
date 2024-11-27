from django.contrib import admin

from materials.models import Course, Module, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
