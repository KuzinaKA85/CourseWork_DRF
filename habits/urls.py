from django.urls import path

from habits.apps import HabitsConfig
from habits import views

app_name = HabitsConfig.name

urlpatterns = [
    # Мои привычки (список и создание)
    path("", views.HabitListCreateView.as_view(), name="habit-list"),
    # Детали привычки (просмотр, редактирование, удаление)
    path("<int:pk>/", views.HabitDetailView.as_view(), name="habit-detail"),
    # Публичные привычки (только просмотр)
    path("public/", views.PublicHabitListView.as_view(), name="habit-public"),
]
