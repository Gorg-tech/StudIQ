from rest_framework import serializers
from .models import Quiz, Question, AnswerOption, Lernset, QuizProgress, Achievement, QuizSession, Feedback, Studiengang, Modul

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
                 'rating_score', 'rating_count', 'avg_time_spent', 
                 'is_public', 'lernset', 'questions']

class LernsetSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lernset
        fields = ['id', 'title', 'description', 'created_at', 'created_by', 'modul', 'quizzes']

class QuizProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizProgress
        fields = ['id', 'quiz', 'correct_answers', 'wrong_answers', 
                 'last_reviewed', 'strength_score']
        
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'unlock_criteria', 'icon_url']
        
class QuizSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSession
        fields = ['id', 'quiz', 'start_time', 'end_time', 'score', 'mode']
        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'quiz', 'rating', 'comment', 'submitted_at']

class StudiengangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studiengang
        fields = '__all__'

class ModulSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modul
        fields = '__all__'