from rest_framework import serializers
from .models import MoodEntry

from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



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


#for signup

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        value = value.lower().strip()
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

#signup serializer 
from django.contrib.auth.password_validation import validate_password

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")

        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            username=validated_data.get('username', ''),
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    