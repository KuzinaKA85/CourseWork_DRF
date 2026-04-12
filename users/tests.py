from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserRegistrationTests(APITestCase):
    """Тесты для регистрации пользователя"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.register_url = reverse("users:register")  # URL для регистрации

    def test_register_user_success(self):
        """Тест: успешная регистрация нового пользователя"""
        data = {
            "email": "test_5@example.com",
            "password": "testpass123",
            "phone_number": "+79123456789",
        }
        response = self.client.post(self.register_url, data)

        # Проверяем, что регистрация прошла успешно (код 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что пользователь создался в базе
        self.assertTrue(User.objects.filter(email="test_5@example.com").exists())

    def test_register_user_invalid_email(self):
        """Тест: регистрация с невалидным email"""
        data = {"email": "not-an-email", "password": "testpass123"}
        response = self.client.post(self.register_url, data)

        # Должна быть ошибка 400 (неправильные данные)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
