from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


class Habit(models.Model):
    """Модель привычки"""

    # Кто создал привычку
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
        help_text="Владелец привычки",
    )
    # Место выполнеия
    place = models.CharField(
        max_length=200,
        verbose_name="Место",
        help_text="Где вы будете выполнять привычку (например: 'Дом', 'Офис', 'Спортзал'",
    )

    # Время, в которое выполняем привычку
    time = models.TimeField(
        verbose_name="Время",
        help_text="Во сколько выполнять привычку (например: 07:00, 15:30, 21:00",
    )

    # Действие (привычка)
    action = models.CharField(
        max_length=300,
        verbose_name="Действие",
        help_text="Что нужно сделать (например: 'Сделать дыхательную гимнастику', 'Выпить стакан воды')",
    )

    # Признак приятной привычки (это вознаграждение)
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Отметьте, если это приятная привычка, которая будет вознаграждением за выполнение полезной привычки",
    )

    # Связанная привычка (только для полезных привычек)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Выберите приятную привычку, которая будет вознаграждением после выполнения полезной привычки",
    )

    # Периодичность в днях (1-7)
    periodicity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность (дни)",
        help_text="Как часто выполнять привычку (1 = каждый день, 7 = 1 раз в неделю)",
    )

    # Вознаграждение
    reward = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Чем себя вознаградить (например: 'Съесть вкусный йогурт', 'Послушать любимую музыку', "
        "'Посмотреть сериал')",
    )

    # Время выполнения в секундах
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name="Время на выполнение (сек)",
        help_text="Сколько времени займет выполнение (не более 120 секунд (2 минуты))",
    )

    # Публичность привычки
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная",
        help_text="Могут ли другие пользователи видеть эту привычку (для вдохновения)",
    )

    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]
