from rest_framework.serializers import ValidationError


class HabitValidator:
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):

        related_habit = value.get(self.fields[0])
        reward = value.get(self.fields[1])
        is_pleasant_habit = value.get(self.fields[2])
        action_time = value.get(self.fields[3])

        if related_habit and reward:
            raise ValidationError("Нельзя одновременно указать связанную привычку и вознаграждение.")

        if is_pleasant_habit and (reward or related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

        if action_time.total_seconds() > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")

        if related_habit and not related_habit.is_pleasant_habit:
            raise ValidationError("Связанная привычка должна быть приятной.")
