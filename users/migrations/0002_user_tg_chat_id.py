# Generated by Django 5.1.6 on 2025-02-15 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="tg_chat_id",
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Телеграм chat_id"),
        ),
    ]
