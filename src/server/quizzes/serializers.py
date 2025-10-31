from rest_framework import serializers
from .models import Quiz, Question, AnswerOption, Lernset, QuizProgress, Achievement, QuizSession, Feedback, Studiengang, Modul

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True)
    quiz = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'answer_options', 'quiz']

class QuizSerializer(serializers.ModelSerializer):
    lernset_title = serializers.CharField(source='lernset.title', read_only=True)
    questions = QuestionSerializer(many=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_at', 'created_by',
            'rating_score', 'rating_count', 'avg_time_spent', 
            'is_public', 'lernset', 'lernset_title', 'questions'
        ]
        
    def create(self, validated_data):
        # create Quiz with nested Questions and AnswerOptions
        questions_data = validated_data.pop('questions', [])
        
        quiz = Quiz.objects.create(**validated_data)
        
        for question_data in questions_data:
            status = question_data.pop('_status', None)  # Pop _status to avoid field error
            question_id = question_data.pop('id', None)  # Pop id for new questions
            answer_options = question_data.pop('answer_options', [])
            question = Question.objects.create(quiz=quiz, **question_data)
            
            for answer_data in answer_options:
                answer_data_copy = answer_data.copy()
                answer_data_copy.pop('id', None)  # Pop id since model has no id field
                AnswerOption.objects.create(question=question, **answer_data_copy)
        
        return quiz
        
    # untested
    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        # Update Quiz fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Verarbeite Questions basierend auf ihrem Status
        for question_data in questions_data:
            status = question_data.pop('_status', None)
            question_id = question_data.pop('id', None)
            answer_options = question_data.pop('answer_options', [])
            
            if status == 'new':
                question = Question.objects.create(quiz=instance, **question_data)
                for answer_data in answer_options:
                    AnswerOption.objects.create(question=question, **answer_data)
                    
            elif status == 'edited':
                if question_id:
                    question = Question.objects.get(id=question_id)
                    for attr, value in question_data.items():
                        setattr(question, attr, value)
                    question.save()
                    
                    # Aktualisiere oder erstelle AnswerOptions
                    current_answers = set(question.answer_options.values_list('id', flat=True))
                    updated_answers = set()
                    
                    for answer_data in answer_options:
                        answer_id = answer_data.get('id')
                        if answer_id:
                            answer = AnswerOption.objects.get(id=answer_id)
                            for attr, value in answer_data.items():
                                setattr(answer, attr, value)
                            answer.save()
                            updated_answers.add(answer_id)
                        else:
                            answer_data_copy = answer_data.copy()
                            answer_data_copy.pop('id', None)
                            AnswerOption.objects.create(question=question, **answer_data_copy)
                    
                    # Lösche nicht mehr vorhandene Antworten
                    to_delete = current_answers - updated_answers
                    AnswerOption.objects.filter(id__in=to_delete).delete()
                    
            elif status == 'deleted':
                if question_id:
                    Question.objects.filter(id=question_id).delete()
        
        return instance

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
    modul = ModulShortSerializer(read_only=True)
    quiz_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Lernset
        fields = ['id', 'title', 'description', 'created_at', 'modul', 'quizzes', 'quiz_count']
        
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
