from django.urls import path

from habits.apps import HabitsConfig
from users.urls import urlpatterns

app_name = HabitsConfig.name

urlpatterns = []