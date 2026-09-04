from rest_framework import serializers
from django.db import models
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    link = serializers.URLField(
        required=False,
        allow_blank=True,
        validators=[validate_youtube_url]  # ⬅️ ДОБАВЛЕН ВАЛИДАТОР
    )

    class Meta:
        model = Lesson
        fields = [
            'id', 'name', 'description', 'link',
            'course', 'owner', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()  # ⬅️ НОВОЕ ПОЛЕ
    lessons_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'description', 'owner',
            'created_at', 'updated_at', 'lessons_count', 'is_subscribed'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_is_subscribed(self, obj):
        """Проверка подписки текущего пользователя на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False


class CourseDetailSerializer(CourseSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['lessons']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'created_at']
        read_only_fields = ['user', 'created_at']

