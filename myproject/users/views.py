from rest_framework import viewsets, status, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Payment
from .serializers import (
    UserSerializer, UserDetailSerializer,
    UserRegistrationSerializer, PaymentSerializer
)
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Регистрация доступна всем
            return [permissions.AllowAny()]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Пользователь может видеть только свой профиль
        if instance != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'У вас нет прав для просмотра этого профиля.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Вы можете редактировать только свой профиль.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Вы можете удалить только свой профиль.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Создаем JWT токены для нового пользователя
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data.get('username'))
            response.data['user'] = UserSerializer(user).data
        return response


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'paid_course': ['exact'],
        'paid_lesson': ['exact'],
        'payment_method': ['exact'],
    }
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)
    