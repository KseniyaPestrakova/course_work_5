from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите email")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон", help_text="Укажите номер телефона"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

