from django.db import models

from users.models import User


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
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users", verbose_name="Автор привычки")
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, related_name="places",
                              verbose_name="Место выполнения привычки")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant_habit = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name="related_to", verbose_name="Связанная привычка")
    period = models.CharField(max_length=12, choices=PERIOD_CHOICES, verbose_name="Периодичность")
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    action_time = models.DurationField(verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
