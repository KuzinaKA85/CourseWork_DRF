from rest_framework.exceptions import ValidationError


def validate_time_to_complete(value):
    """Время выполнения не больше 120 секунд"""
    if value > 120:
        raise ValidationError(
            f"Время выполнения не может превышать 120 секунд."
            f"Вы указали {value} секунд."
        )


def validate_periodicity(value):
    """Периодичность от 1 до 7 дней"""
    if value < 1 or value > 7:
        raise ValidationError(
            f"Периодичность должна быть от 1 до 7 дней." f"Вы указали {value} дней."
        )


def validate_no_both_reward_and_related(habit):
    """Нельзя одновременно выбрать reward и related_habit"""
    if habit.reward and habit.related_habit:
        raise ValidationError(
            "Нельзя одновременно указать вознаграждение и связанную привычку. "
            "Выберите что-то одно."
        )


def validate_related_habit_is_pleasant(habit):
    """Связанная привычка должна быть приятной"""
    if habit.related_habit and not habit.related_habit.is_pleasant:
        raise ValidationError(
            "Связанная привычка должна быть приятной. "
            "Выберите привычку с признаком 'Приятная привычка'."
        )


def validate_pleasant_habit_no_reward_or_related(habit):
    """У приятной привычки не может быть reward или related_habit"""
    if habit.is_pleasant:
        if habit.reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")
        if habit.related_habit:
            raise ValidationError(
                "У приятной привычки не может быть связанной привычки."
            )
