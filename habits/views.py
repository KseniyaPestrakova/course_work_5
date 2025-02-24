from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit, Place
from habits.paginators import HabitsPaginator
from habits.permissions import IsAuthor
from habits.serializers import HabitSerializer, PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.user = self.request.user

        if habit.user.tg_chat_id:

            habit.last_reminder = timezone.now()
            habit.save()


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    pagination_class = HabitsPaginator

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]


class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitsPaginator

    def get_queryset(self):
        # Возвращаем только публичные привычки
        return Habit.objects.filter(is_public=True)
