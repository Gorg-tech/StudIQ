from rest_framework import serializers
from .models import Quiz, Question, AnswerOption, Lernset

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'answer_options', 'quiz']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'created_by',
                 'rating_score', 'rating_count', 'estimated_duration', 
                 'is_published', 'lernset', 'questions']

class LernsetSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lernset
        fields = ['id', 'title', 'description', 'created_at', 'created_by', 'modul', 'quizzes']