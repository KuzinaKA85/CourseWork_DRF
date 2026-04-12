from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit


class HabitTests(APITestCase):
    """Тесты для привычек"""

    def setUp(self):
        """Подготовка перед каждым тестом"""

        self.user = User(email="test@example.com")
        self.user.set_password("testpass123")
        self.user.save()

        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

        # URL для работы с привычками
        self.habits_list_url = reverse("habits:habit-list")
        self.public_habits_url = reverse("habits:habit-public")

        # Создаем тестовую привычку
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="09:00:00",
            action="Сделать зарядку",
            is_pleasant=False,
            duration=60,
            is_public=True,
        )

        # URL для деталей привычки
        self.habit_detail_url = reverse("habits:habit-detail", args=[self.habit.id])

    def test_list_habits_authenticated(self):
        """Тест: авторизованный пользователь видит свои привычки"""
        response = self.client.get(self.habits_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Сделать зарядку")

    def test_list_habits_unauthenticated(self):
        """Тест: неавторизованный пользователь не видит привычки"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.habits_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_habits(self):
        """Тест: пользователь видит только свои привычки"""
        # Создаем другого пользователя
        other_user = User(email="other@example.com")
        other_user.set_password("otherpass")
        other_user.save()

        # Создаем привычку для другого пользователя
        Habit.objects.create(
            user=other_user,
            place="Офис",
            time="10:00:00",
            action="Выпить воды",
            duration=30,
            is_public=False,
        )

        response = self.client.get(self.habits_list_url)

        # Должна быть только 1 привычка (своя)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Сделать зарядку")

    def test_create_habit_success(self):
        """Тест: успешное создание привычки"""
        data = {
            "place": "Парк",
            "time": "18:00:00",
            "action": "Прогулка",
            "duration": 30,
            "periodicity": 1,
            "is_public": False,
        }
        response = self.client.post(self.habits_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(response.data["action"], "Прогулка")

    def test_create_habit_duration_too_long(self):
        """Тест: создание привычки с длительностью больше 120 секунд"""
        data = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Медитация",
            "duration": 200,
            "periodicity": 1,
        }
        response = self.client.post(self.habits_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("duration", str(response.data))

    def test_create_habit_invalid_periodicity(self):
        """Тест: создание привычки с неверной периодичностью (больше 7)"""
        data = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Чтение",
            "duration": 60,
            "periodicity": 14,
        }
        response = self.client.post(self.habits_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_reward_and_related_together(self):
        """Тест: нельзя одновременно указать reward и related_habit"""
        # Создаем приятную привычку для связи
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Посмотреть сериал",
            is_pleasant=True,
            duration=30,
        )

        data = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Уборка",
            "duration": 60,
            "reward": "Съесть конфету",
            "related_habit": pleasant_habit.id,
            "periodicity": 1,
        }
        response = self.client.post(self.habits_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_habit_owner(self):
        """Тест: владелец может обновить свою привычку"""
        data = {"action": "Новое действие"}
        response = self.client.patch(self.habit_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Новое действие")

    def test_update_habit_not_owner(self):
        """Тест: чужой пользователь не может обновить привычку"""
        # Создаем другого пользователя
        other_user = User(email="other@example.com")
        other_user.set_password("otherpass")
        other_user.save()

        self.client.force_authenticate(user=other_user)

        data = {"action": "Попытка взлома"}
        response = self.client.patch(self.habit_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_habit_owner(self):
        """Тест: владелец может удалить свою привычку"""
        response = self.client.delete(self.habit_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_delete_habit_not_owner(self):
        """Тест: чужой пользователь не может удалить привычку"""
        other_user = User(email="other@example.com")
        other_user.set_password("otherpass")
        other_user.save()

        self.client.force_authenticate(user=other_user)

        response = self.client.delete(self.habit_detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habits_visible_to_all(self):
        """Тест: публичные привычки видны всем (даже без авторизации)"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.public_habits_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_private_habit_not_in_public_list(self):
        """Тест: приватные привычки не показываются в публичном списке"""
        # Создаем приватную привычку
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="22:00:00",
            action="Спать",
            duration=60,
            is_public=False,
        )

        response = self.client.get(self.public_habits_url)

        # Проверяем, что приватная привычка не попала в список
        actions = [item["action"] for item in response.data["results"]]
        self.assertNotIn("Спать", actions)
