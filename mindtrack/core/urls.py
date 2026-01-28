from django.urls import path
from .views import MoodEntryCreateView, MoodEntryListView

urlpatterns = [
    path('moods/create/', MoodEntryCreateView.as_view()),
    path('moods/', MoodEntryListView.as_view()),
]
