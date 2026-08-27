from rest_framework import serializers
from .models import Payment, User
from courses.models import Course, Lesson


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    course_title = serializers.CharField(source='paid_course.title', read_only=True, allow_null=True)
    lesson_title = serializers.CharField(source='paid_lesson.title', read_only=True, allow_null=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_email', 'payment_date',
            'paid_course', 'course_title',
            'paid_lesson', 'lesson_title',
            'amount', 'payment_method'
        ]
        read_only_fields = ['payment_date']
