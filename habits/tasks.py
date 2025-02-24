from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def schedule_habit_reminders():
    habits = Habit.objects.all()
    now = timezone.now()

    for habit in habits:
        if habit.user.tg_chat_id and habit.last_reminder and habit.last_reminder < now:

            message = f"Пора выполнить привычку: {habit.action}"
            send_telegram_message(message, habit.user.tg_chat_id)
            if habit.period == "every_hour":
                habit.last_reminder += timedelta(hours=1)
            elif habit.period == "four_times_a_day":
                habit.last_reminder += timedelta(hours=6)
            elif habit.period == "twice_a_day":
                habit.last_reminder += timedelta(hours=12)
            elif habit.period == "daily":
                habit.last_reminder += timedelta(days=1)
            elif habit.period == "once_every_three_days":
                habit.last_reminder += timedelta(days=3)
            elif habit.period == "weekly":
                habit.last_reminder += timedelta(weeks=1)
            else:
                continue
        else:
            continue
        habit.save()
