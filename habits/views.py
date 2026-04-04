from rest_framework import generics, permissions
from habits.models import Habit
from habits.serializers import HabitSerializer, HabitPublicSerializer
from habits.pagination import HabitPagination


class HabitListCreateView(generics.ListCreateAPIView):
    """Список привычек и создание"""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, редактирование, удаление"""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Публичные привычки"""

    serializer_class = HabitPublicSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
