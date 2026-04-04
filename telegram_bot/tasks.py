import requests
from django.utils import timezone
from celery import shared_task
from django.conf import settings
from habits.models import Habit


@shared_task
def check_habits():
    """Проверка привычек каждую минуту"""

    now = timezone.now()

    # Ищем привычки на это время
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)

    for habit in habits:
        send_reminder.delay(habit.id)


@shared_task
def send_reminder(habit_id):
    """Отправка напоминания"""
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user

        if not user.telegram_chat_id:
            return

        # Отправляем сообщение
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        message = f"Напоминание! {habit.action} в {habit.place} в {habit.time}"
        requests.post(url, json={"chat_id": user.telegram_chat_id, "text": message})

    except Exception as e:
        print(f"Ошибка отправки напоминания: {e}")
