from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    PLAN_CHOICES = (
        ('free', 'Free'),
        ('premium', 'Premium'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='free')
    mood_analysis_used = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan}"


class MoodEntry(models.Model):
    MOOD_CHOICES = (
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('angry', 'Angry'),
        ('anxious', 'Anxious'),
        ('stressed', 'Stressed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    detected_mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    confidence_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.detected_mood} ({self.created_at.date()})"


class TestModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
