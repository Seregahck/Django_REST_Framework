from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from .views import UserViewSet, UserRegistrationView, PaymentViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    # JWT эндпоинты
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Регистрация
    path('api/register/', UserRegistrationView.as_view(), name='user_register'),

    # Включаем роутер
    path('', include(router.urls)),
]
