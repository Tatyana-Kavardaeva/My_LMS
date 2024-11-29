from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'


class IsUser(permissions.BasePermission):
    """ Разрешение, которое позволяет пользователю редактировать только свой профиль. """
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwner(permissions.BasePermission):
    """ Проверяет, является ли пользователь владельцем объекта. """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

#
#
# class IsAdmin(permissions.BasePermission):
#     """ Проверяет, является ли пользователь администратором. """
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='Admin').exists()
#
#
# class IsTeacher(permissions.BasePermission):
#     """ Проверяет, является ли пользователь преподавателем. """
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='Teacher').exists()
#
#
# class IsStudent(permissions.BasePermission):
#     """ Проверяет, является ли пользователь студентом. """
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='Student').exists()
#
#
# class IsOwner(permissions.BasePermission):
#     """ Проверяет, является ли пользователь владельцем объекта. """
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user
#
#

