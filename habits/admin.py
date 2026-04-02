from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "action",
        "place",
        "time",
        "is_pleasant",
        "reward",
        "related_habit",
        "duration",
        "periodicity",
        "user",
        "is_public",
        "created_at"
    )
    list_filter = ("action", "user", "is_public", "created_at")
    search_fields = ("action", "user", "is_public")