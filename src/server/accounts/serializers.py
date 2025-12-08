"""
Object Serializer for account related objects defined in models.py.

This file contains all serializer classes for account related objects.
Serializers convert django models into JSON and back, validate data and
support nested structures for more complex objects, such as quizzes containing questions.
"""

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, StudyDay
from quizzes.models import Studiengang

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User objects, representing user profiles and statistics.
    Adds the study program name for display purposes.
    """
    studiengang_name = serializers.CharField(source='studiengang.name', read_only=True)

    class Meta:
        """
        Meta class defining the model and fields to be serialized for User.
        Sets certain fields as read-only.
        """
        model = User
        fields = ['id', 'username', 'email', 'role', 'iq_score', 
                 'correct_answers', 'wrong_answers', 'solved_quizzes', 
                 'streak', 'studiengang', 'studiengang_name']
        read_only_fields = ['id', 'iq_score', 'correct_answers', 
                           'wrong_answers', 'solved_quizzes', 'streak']

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializes registration data for creating new User accounts.
    Validates password and requires a valid Studiengang (study program) ID.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # Require a valid Studiengang ID on registration
    studiengang = serializers.PrimaryKeyRelatedField(
        queryset=Studiengang.objects.all(),
        required=True,
        error_messages={
            'required': 'Studiengang ist erforderlich.',
            'does_not_exist': 'Ungültiger Studiengang.',
            'incorrect_type': 'Studiengang muss eine gültige ID sein.'
        }
    )

    class Meta:
        """
        Meta class defining the model and fields to be serialized for registration.
        """
        model = User
        fields = ['username', 'email', 'password', 'studiengang']

    def create(self, validated_data):
        """
        Creates a new User instance with the provided validated data.
        """
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializes login credentials for user authentication.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class StudyDaySerializer(serializers.ModelSerializer):
    """
    Serializes StudyDay objects, representing a user's study activity on a specific date.
    """
    class Meta:
        """
        Meta class defining the model and fields to be serialized for StudyDay.
        """
        model = StudyDay
        fields = ['date']