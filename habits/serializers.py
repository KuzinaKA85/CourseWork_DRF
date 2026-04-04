from rest_framework import serializers
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычек"""

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration",
            "is_public",
            "created_at",
        ]
        read_only_fields = [
            "user",
            "created_at",
        ]

    def validate(self, data):
        """Валидация при создании/обновлении"""

        # Проверка времени выполнения, не больше 120 сек
        if data.get("duration", 0) > 120:
            raise serializers.ValidationError(
                {"duration": "Время выполнения не может превышать 120 секунд."}
            )

        # Проверка периодичности от 1 до 7 дней
        periodicity = data.get("periodicity", 1)
        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError(
                {"periodicity": "Периодичность должна быть от 1 до 7 дней."}
            )

        # Нельзя одновременно указать reward и related_habit
        if data.get("reward") and data.get("related_habit"):
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "Нельзя одновременно указать вознаграждение "
                        "и связанную привычку."
                    ]
                }
            )

        # Связанная привычка должна быть приятной
        if data.get("related_habit"):
            related = data["related_habit"]
            if not related.is_pleasant:
                raise serializers.ValidationError(
                    {"related_habit": "Связанная привычка должна быть приятной."}
                )

        # У приятной привычки не может быть reward или related_habit
        if data.get("is_pleasant"):
            if data.get("reward"):
                raise serializers.ValidationError(
                    {"reward": "У приятной привычки не может быть вознаграждения."}
                )
            if data.get("related_habit"):
                raise serializers.ValidationError(
                    {
                        "related_habit": "У приятной привычки не может быть связанной привычки."
                    }
                )

        return data


class HabitPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек (только чтение)"""

    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Habit
        fields = [
            "id",
            "user_email",
            "place",
            "time",
            "action",
            "is_pleasant",
            "periodicity",
            "duration",
            "created_at",
        ]
        read_only_fields = fields
