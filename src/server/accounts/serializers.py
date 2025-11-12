from rest_framework import serializers
from .models import User, StudyDay
from django.contrib.auth.password_validation import validate_password
from quizzes.models import Studiengang

class UserSerializer(serializers.ModelSerializer):
    studiengang_name = serializers.CharField(source='studiengang.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'iq_level', 
                 'correct_answers', 'wrong_answers', 'solved_quizzes', 
                 'streak', 'studiengang', 'studiengang_name']
        read_only_fields = ['id', 'iq_level', 'correct_answers', 
                           'wrong_answers', 'solved_quizzes', 'streak']

class RegisterSerializer(serializers.ModelSerializer):
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
        model = User
        fields = ['username', 'email', 'password', 'studiengang']
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class StudyDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyDay
        fields = ['date']