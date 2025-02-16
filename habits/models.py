from django.db import models

from config import settings


class Place(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название места")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class Habit(models.Model):
    PERIOD_CHOICES = [
        ("every_hour", "Каждый час"),
        ("four_times_a_day", "Четыре раза в день"),
        ("twice_a_day", "Дважды в день"),
        ("daily", "Ежедневно"),
        ("once_every_three_days", "Раз в три дня"),
        ("weekly", "Еженедельно"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="users",
        verbose_name="Автор привычки",
    )
    place = models.ForeignKey(
        Place,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="places",
        verbose_name="Место выполнения привычки",
    )
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant_habit = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="related_to",
        verbose_name="Связанная привычка",
    )
    period = models.CharField(max_length=21, choices=PERIOD_CHOICES, verbose_name="Периодичность")
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    action_time = models.DurationField(verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")
    last_reminder = models.DateTimeField(blank=True, null=True, verbose_name="Последнее напоминание в Телеграм")

    def __str__(self):
        return f"Я буду {self.action} {self.period} {self.place}."

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
