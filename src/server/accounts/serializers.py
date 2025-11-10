from rest_framework import serializers
from .models import User, StudyDay
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'iq_level', 
                 'correct_answers', 'wrong_answers', 'solved_quizzes', 
                 'streak', 'studiengang', 'semester']
        read_only_fields = ['id', 'iq_level', 'correct_answers', 
                           'wrong_answers', 'solved_quizzes', 'streak']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'studiengang', 'semester']
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class StudyDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyDay
        fields = ['id', 'user', 'date']
        read_only_fields = ['id', 'user']