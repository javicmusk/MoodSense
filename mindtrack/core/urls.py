from django.urls import path
from .views import MoodEntryListCreateView

from .views import RegisterView


urlpatterns = [
    path('auth/signup/', RegisterView.as_view(), name='signup'),

    path('moods/', MoodEntryListCreateView.as_view(), name='moods'),
    
]
