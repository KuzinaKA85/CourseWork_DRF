from rest_framework import serializers
from habits.models import Habit
from habits.validators import validate_time_to_complete, validate_periodicity


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

        # Проверка времени выполнения
        if data.get("duration"):
            validate_time_to_complete(data["duration"])

        # Проверка периодичности
        if data.get("periodicity"):
            validate_periodicity(data["periodicity"])

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
