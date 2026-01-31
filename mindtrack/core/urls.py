from django.urls import path
from .views import (
    SignupView,
    MeView,
    MoodEntryListCreateView,
)
from .views import AnalyzeMoodView

urlpatterns = [
    # Auth
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/me/', MeView.as_view(), name='me'),

    # Mood
    path('moods/', MoodEntryListCreateView.as_view(), name='moods'),
    path("moods/analyze/", AnalyzeMoodView.as_view()),
]



