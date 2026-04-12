import time

import requests
from django.conf import settings
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Запуск telegram бота"""

    def handle(self, *args, **options):
        self.stdout.write("Telegram бот запущен...")

        # URL для получения сообщений
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates"

        last_id = 0

        while True:
            try:
                resp = requests.get(url, params={"offset": last_id + 1, "timeout": 30})
                data = resp.json()
                if data["ok"]:
                    for update in data["result"]:
                        # Обрабатываем сообщение
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"].get("text", "")

                        if text == "/start":
                            self.send_message(chat_id, "Напишите Ваш email")
                        elif "@" in text and "." in text:
                            self.save_user(chat_id, text)
                            self.send_message(
                                chat_id,
                                "Готово! Теперь Вы будете получать напоминания!",
                            )
                        else:
                            self.send_message(chat_id, "Напишите /start")

                        last_id = update["update_id"]

                time.sleep(1)
            except Exception as e:
                self.stdout.write(f"Ошибка: {e}")
                time.sleep(5)

    def send_message(self, chat_id, text):
        """Отправка сообщения"""

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text})

    def save_user(self, chat_id, email):
        """Сохранение chat_id пользователя"""
        try:
            user = User.objects.get(email=email)
            user.telegram_chat_id = str(chat_id)
            user.save()
        except User.DoesNotExist:
            self.send_message(
                chat_id, "Пользователь с таким email не найден. Попробуйте еще раз"
            )
