from rest_framework import serializers

from habits.models import Habit, Place
from habits.validators import HabitValidator


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [HabitValidator(fields=("related_habit", "reward", "is_pleasant_habit", "action_time"))]
