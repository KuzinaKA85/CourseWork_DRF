from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    password = serializers.CharField(
        write_only=True,  # пароль только для записи (не показывается в ответе)
        required=True,
        min_length=6,
        help_text="Пароль (минимум 6 символов)",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "phone_number",
            "avatar",
            "country",
            "is_active",
        ]
        read_only_fields = ["id", "is_active"]

    def create(self, validated_data):
        """Создание пользователя с хешированным паролем"""
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # хешируем пароль
        user.save()
        return user

    def update(self, instance, validated_data):
        """Обновление пользователя"""
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # если меняют пароль - хешируем

        instance.save()
        return instance
