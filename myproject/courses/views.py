from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Course, Lesson, Subscription
from .serializers import (
    CourseSerializer, CourseDetailSerializer,
    LessonSerializer, SubscriptionSerializer
)
from .paginators import CoursePagination, LessonPagination
from .permissions import IsOwnerOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset.annotate(lessons_count=models.Count('lessons'))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination  # ⬅️ ДОБАВЛЕНА ПАГИНАЦИЯ
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionCreateView(generics.CreateAPIView):
    """Эндпоинт для создания подписки"""
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')

        if not course_id:
            return Response(
                {'error': 'Необходимо указать ID курса'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        if Subscription.objects.filter(user=user, course=course).exists():
            return Response(
                {'error': 'Вы уже подписаны на этот курс'},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription = Subscription.objects.create(user=user, course=course)
        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscriptionDeleteView(generics.DestroyAPIView):
    """Эндпоинт для удаления подписки"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        course_id = self.request.data.get('course') or self.request.query_params.get('course')

        if not course_id:
            raise PermissionDenied('Необходимо указать ID курса')

        course = get_object_or_404(Course, id=course_id)
        subscription = get_object_or_404(Subscription, user=user, course=course)

        return subscription

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {'message': 'Подписка успешно удалена'},
                status=status.HTTP_200_OK
            )
        except PermissionDenied as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

