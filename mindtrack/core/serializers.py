from rest_framework import serializers
from .models import MoodEntry


class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = [
            'id',
            'text',
            'detected_mood',
            'confidence_score',
            'created_at',
        ]
