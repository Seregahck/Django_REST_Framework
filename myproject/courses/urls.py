from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, LessonViewSet,
    SubscriptionCreateView, SubscriptionDeleteView
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('subscriptions/create/', SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscriptions/delete/', SubscriptionDeleteView.as_view(), name='subscription-delete'),
]
