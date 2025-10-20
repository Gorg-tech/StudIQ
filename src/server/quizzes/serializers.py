from rest_framework import serializers
from .models import Quiz, Question, AnswerOption, Lernset, QuizProgress, Achievement, QuizSession, Feedback, Studiengang, Modul

class AnswerOptionSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=True)

    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'is_correct', 'question']

class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'answer_options', 'quiz']

class QuizSerializer(serializers.ModelSerializer):
    lernset_title = serializers.CharField(source='lernset.title', read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_at', 'created_by',
            'rating_score', 'rating_count', 'avg_time_spent', 
            'is_public', 'lernset', 'lernset_title', 'questions'
        ]

class QuizForLernsetSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    creator_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_at', 'created_by', 'creator_username',
            'rating_score', 'rating_count', 'avg_time_spent', 
            'is_public', 'lernset', 'question_count'
        ]

    def get_question_count(self, obj):
        return obj.questions.count()

class ModulShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modul
        fields = ['modulId', 'name']

class LernsetSerializer(serializers.ModelSerializer):
    quizzes = QuizForLernsetSerializer(many=True, read_only=True)
    modul = serializers.PrimaryKeyRelatedField(queryset=Modul.objects.all()) 
    modul_detail = ModulShortSerializer(source='modul', read_only=True)
    quiz_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Lernset
        fields = ['id', 'title', 'description', 'created_at', 'modul', 'modul_detail', 'quizzes', 'quiz_count']
        
    def get_quiz_count(self, obj):
        return obj.quizzes.count()
    
    def create(self, validated_data):
        # Need this for POST requests since we changed modul to read_only
        modul_id = self.initial_data.get('modul')
        modul = Modul.objects.get(modulId=modul_id)
        validated_data['modul'] = modul
         return super().create(validated_data)

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

class LernsetForModulSerializer(serializers.ModelSerializer):
    quiz_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Lernset
        fields = ['id', 'title', 'description', 'created_at', 'quiz_count']
        
    def get_quiz_count(self, obj):
        return obj.quizzes.count()

class ModulDetailSerializer(serializers.ModelSerializer):
    lernsets = LernsetForModulSerializer(many=True, read_only=True)
    
    class Meta:
        model = Modul
        fields = '__all__'
