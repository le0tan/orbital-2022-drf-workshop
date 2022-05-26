from rest_framework import viewsets, permissions

from app.models import Course
from app.serializers import CourseSerializer


class CoursePermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        course = obj  # for better code competion in PyCharm
        if request.user.is_superuser:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('app.view_course')
        elif request.method == 'POST':
            return request.user.has_perm('app.add_course')
        elif request.method == 'PUT':
            return request.user.has_perm('app.change_course')
        elif request.method == 'DELETE':
            return request.user.has_perm('app.delete_course')
        return False


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CoursePermissions]
