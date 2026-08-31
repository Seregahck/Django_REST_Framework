from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'course', 'owner', 'owner_username', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner', 'owner_username', 'created_at', 'updated_at', 'lesson_count',
                  'lessons']
        read_only_fields = ['created_at', 'updated_at']

    def get_lesson_count(self, obj):
        return obj.lessons.count()
