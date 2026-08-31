from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModeratorOrOwner, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        # Администратор видит все
        if user.is_staff:
            return Course.objects.all()

        # Модератор видит все курсы для просмотра и изменения
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()

        # Обычный пользователь видит только свои курсы
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        # Проверяем, что модератор не создает курс
        if self.request.user.groups.filter(name='moderators').exists():
            raise PermissionDenied('Модераторы не могут создавать курсы.')
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # Проверяем права на обновление
        instance = self.get_object()
        if not self.request.user.groups.filter(name='moderators').exists():
            if instance.owner != self.request.user:
                raise PermissionDenied('Вы не являетесь владельцем этого курса.')
        serializer.save()

    def perform_destroy(self, instance):
        # Проверяем права на удаление
        if self.request.user.groups.filter(name='moderators').exists():
            raise PermissionDenied('Модераторы не могут удалять курсы.')
        if instance.owner != self.request.user:
            raise PermissionDenied('Вы не являетесь владельцем этого курса.')
        instance.delete()


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'title']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        # Администратор видит все
        if user.is_staff:
            return Lesson.objects.all()

        # Модератор видит все уроки для просмотра и изменения
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()

        # Обычный пользователь видит только свои уроки
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        # Проверяем, что модератор не создает урок
        if self.request.user.groups.filter(name='moderators').exists():
            raise PermissionDenied('Модераторы не могут создавать уроки.')
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # Проверяем права на обновление
        instance = self.get_object()
        if not self.request.user.groups.filter(name='moderators').exists():
            if instance.owner != self.request.user:
                raise PermissionDenied('Вы не являетесь владельцем этого урока.')
        serializer.save()

    def perform_destroy(self, instance):
        # Проверяем права на удаление
        if self.request.user.groups.filter(name='moderators').exists():
            raise PermissionDenied('Модераторы не могут удалять уроки.')
        if instance.owner != self.request.user:
            raise PermissionDenied('Вы не являетесь владельцем этого урока.')
        instance.delete()
