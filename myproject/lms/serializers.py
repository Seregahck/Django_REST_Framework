from rest_framework import serializers
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'lessons_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = (
        'id', 'course', 'course_title', 'title', 'description', 'preview', 'video_url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
