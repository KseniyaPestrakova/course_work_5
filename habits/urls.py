from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import (HabitCreateAPIView, HabitDestroyAPIView, HabitListAPIView, HabitPublicListAPIView,
                          HabitRetrieveAPIView, HabitUpdateAPIView, PlaceViewSet)

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"places", PlaceViewSet, basename="places")

urlpatterns = [
    path("habit/create/", HabitCreateAPIView.as_view(), name="habit-create"),
    path("habit/", HabitListAPIView.as_view(), name="habit-list"),
    path("habit/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit-get"),
    path("habit/update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habit-update"),
    path("habit/delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="habit-delete"),
    path("public_habit/", HabitPublicListAPIView.as_view(), name="public_habit-list"),
] + router.urls
