from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    Регистрация нового пользователя
    Доступно всем (AllowAny)
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Сериализатор сам обрабатывает хеширование пароля
        serializer.save(is_active=True)


class UserViewSet(viewsets.ModelViewSet):
    """
    Управление пользователями (только для админов)
    Просмотр, редактирование, удаление пользователей
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Обычный пользователь видит только себя
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)

