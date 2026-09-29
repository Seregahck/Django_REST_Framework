from django.contrib import admin
from .models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'created_at']
    list_filter = ['owner', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'course', 'owner', 'created_at']
    list_filter = ['course', 'owner', 'created_at']
    search_fields = ['name', 'description', 'link']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'created_at']
    list_filter = ['user', 'course', 'created_at']
    search_fields = ['user__username', 'course__name']
