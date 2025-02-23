from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta
from habits.models import Habit, Place
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro", username="admin", password="12345")
        self.place = Place.objects.create(name="Спортзал")
        self.habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            action="Test",
            period="every_hour",
            reward="Test_reward",
            action_time=timedelta(minutes=1),
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тест на создание привычки с корректными данными"""
        url = reverse("habits:habit-create")
        data = {
            "user": self.user.id,
            "place": self.place.id,
            "action": "Выполнить тренировку",
            "is_pleasant_habit": False,
            "period": "daily",
            "action_time": timedelta(minutes=1),
            "is_public": True,
            "reward": "Съесть протеиновый батончик",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        habit = Habit.objects.get(pk=2)
        self.assertEqual(habit.action, "Выполнить тренировку")
        self.assertEqual(habit.period, "daily")
        self.assertEqual(habit.place, self.place)

    def test_habit_with_invalid_action_time(self):
        """Тест, когда время на выполнение привычки превышает 120 секунд"""
        url = reverse("habits:habit-create")
        data = {
            "user": self.user.id,
            "place": self.place.id,
            "action": "Выполнить тренировку",
            "is_pleasant_habit": False,
            "period": "daily",
            "action_time": timedelta(minutes=3),
            "is_public": True,
            "reward": "Съесть протеиновый батончик",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Время выполнения не должно превышать 120 секунд.", response.data["non_field_errors"])

    def test_habit_with_reward_and_related_habit(self):
        """Тест, когда указывается и вознаграждение, и связанная привычка"""
        related_habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            action="related_test",
            period="daily",
            action_time=timedelta(minutes=1),
            is_pleasant_habit=True,
        )
        url = reverse("habits:habit-create")
        data = {
            "user": self.user.id,
            "place": self.place.id,
            "action": "Выполнить тренировку",
            "is_pleasant_habit": False,
            "period": "daily",
            "action_time": timedelta(minutes=2),
            "related_habit": related_habit.id,
            "reward": "Съесть протеиновый батончик",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя одновременно указать связанную привычку и вознаграждение.", response.data["non_field_errors"]
        )

    def test_pleasant_habit_with_reward(self):
        """Тест, когда приятная привычка указана с вознаграждением"""
        url = reverse("habits:habit-create")
        data = {
            "user": self.user.id,
            "place": self.place.id,
            "action": "Выполнить тренировку",
            "is_pleasant_habit": True,
            "period": "daily",
            "action_time": timedelta(minutes=2),
            "reward": "Съесть протеиновый батончик",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть вознаграждения или связанной привычки.",
            response.data["non_field_errors"],
        )

    def test_related_habit_not_pleasant(self):
        """Тест, когда связанная привычка не является приятной"""
        related_habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            action="not_pleasant_test",
            period="daily",
            action_time=timedelta(minutes=2),
            is_pleasant_habit=False,
        )
        url = reverse("habits:habit-create")
        data = {
            "user": self.user.id,
            "place": self.place.id,
            "action": "Выполнить тренировку",
            "is_pleasant_habit": False,
            "period": "daily",
            "action_time": timedelta(minutes=2),
            "related_habit": related_habit.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Связанная привычка должна быть приятной.", response.data["non_field_errors"])

    def test_update_habit(self):
        """Тест на обновление привычки"""
        url = reverse("habits:habit-update", args=[self.habit.id])
        data = {
            "user": self.user.id,
            "place": self.place.id,
            "action": "Тест_обновление",
            "is_pleasant_habit": False,
            "period": "twice_a_day",
            "action_time": timedelta(minutes=2),
            "is_public": False,
            "reward": "Test_reward",
        }
        response = self.client.put(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Тест_обновление")
        self.assertEqual(data.get("period"), "twice_a_day")
        self.assertEqual(data.get("reward"), "Test_reward")

    def test_delete_habit(self):
        """Тест на удаление привычки"""
        url = reverse("habits:habit-delete", args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
