"""
Object Serializer for quiz related objects defined in models.py.

This file contains all serializer classes for quiz related objects.
Serializers convert django models into JSON and back, validate data and
support nested structures for more complex objects, such as quizzes containing questions.
"""

from rest_framework import serializers
from .models import Quiz, Question, AnswerOption, Lernset,\
                    QuizSession, Feedback, Studiengang, Modul

class AnswerOptionSerializer(serializers.ModelSerializer):
    """
    Serializes AnswerOption objects, representing possible answers for a quiz question.
    Handles creation, update, and validation of answer options, including correctness flag.
    """
    _status = serializers.CharField(write_only=True, required=False)

    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = AnswerOption
        fields = ['id', 'text', 'is_correct', '_status']

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializes Question objects, including nested answer options.
    Used for creating, updating, and retrieving quiz questions with their possible answers.
    """
    answer_options = AnswerOptionSerializer(many=True)
    quiz = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.UUIDField(required=False)
    _status = serializers.CharField(write_only=True, required=False)

    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Question
        fields = ['id', 'text', 'type', 'answer_options', 'quiz', '_status']

class QuizSerializer(serializers.ModelSerializer):
    """
    Serializes Quiz objects, including nested questions and answer options.
    Handles creation and update of quizzes with all related data.
    Adds extra fields for frontend display, such as lernset title and creator.
    """
    lernset_title = serializers.CharField(source='lernset.title', read_only=True)
    modul_name = serializers.CharField(source='lernset.modul.name', read_only=True)
    modul_id = serializers.CharField(source='lernset.modul.modulId', read_only=True)
    questions = QuestionSerializer(many=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_at', 'created_by', 'avg_time_spent', 
            'is_public', 'lernset', 'lernset_title', 'modul_name', 'modul_id', 'questions'
        ]

    def create(self, validated_data):
        """
        create Quiz with nested Questions and AnswerOptions
        """
        questions_data = validated_data.pop('questions', [])
        # Require at least 3 questions to create a quiz
        if len(questions_data) < 3:
            raise serializers.ValidationError({
                'questions': 'Ein Quiz muss mindestens 3 Fragen enthalten.'
            })

        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            _ = question_data.pop('_status', None)  # Pop _status to avoid field error
            _ = question_data.pop('id', None)  # Pop id for new questions
            answer_options = question_data.pop('answer_options', [])
            question = Question.objects.create(quiz=quiz, **question_data)

            for answer_data in answer_options:
                answer_data_copy = answer_data.copy()
                answer_data_copy.pop('id', None)  # Pop id since model has no id field
                answer_data_copy.pop('_status', None)  # Pop _status as it's not a model field
                AnswerOption.objects.create(question=question, **answer_data_copy)

        return quiz

    def update(self, instance, validated_data):
        """
        update Quiz based on status of the questions and their answer_options (nested)
        """
        questions_data = validated_data.pop('questions', [])
        # Update Quiz fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Verarbeite Questions basierend auf ihrem Status
        for question_data in questions_data:
            status = question_data.pop('_status', None)
            question_id = question_data.get('id') # Use .get() to avoid removing it
            answer_options_data = question_data.pop('answer_options', [])

            if status == 'new':
                # Remove temporary frontend ID
                question_data.pop('id', None)
                question = Question.objects.create(quiz=instance, **question_data)
                for answer_data in answer_options_data:
                    answer_data.pop('id', None)
                    answer_data.pop('_status', None)
                    AnswerOption.objects.create(question=question, **answer_data)

            elif status == 'edited' and question_id:
                question = Question.objects.get(id=question_id, quiz=instance)
                question.text = question_data.get('text', question.text)
                question.type = question_data.get('type', question.type)
                question.save()

                # Update or create AnswerOptions
                existing_answer_ids = set(question.answer_options.values_list('id', flat=True))
                received_answer_ids = set()

                for answer_data in answer_options_data:
                    answer_id = answer_data.get('id')
                    answer_status = answer_data.pop('_status', 'unchanged')

                    if answer_status == 'new':
                        answer_data.pop('id', None)
                        AnswerOption.objects.create(question=question, **answer_data)
                    elif answer_status == 'edited' and answer_id in existing_answer_ids:
                        answer_instance = AnswerOption.objects.get(id=answer_id)
                        answer_instance.text = answer_data.get('text', answer_instance.text)
                        answer_instance.is_correct = answer_data.get('is_correct',
                                                                     answer_instance.is_correct)
                        answer_instance.save()
                        received_answer_ids.add(answer_id)
                    elif answer_status == 'deleted' and answer_id in existing_answer_ids:
                        AnswerOption.objects.filter(id=answer_id).delete()
                    elif answer_id in existing_answer_ids:
                        received_answer_ids.add(answer_id)

            elif status == 'deleted' and question_id:
                Question.objects.filter(id=question_id, quiz=instance).delete()

        return instance

class QuizForLernsetSerializer(serializers.ModelSerializer):
    """
    Serializes Quiz objects for use within a Lernset context.
    Includes question count and creator information for summary views.
    """
    question_count = serializers.SerializerMethodField()
    creator_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_at', 'created_by', 'creator_username', 'avg_time_spent', 
            'is_public', 'lernset', 'question_count'
        ]

    def get_question_count(self, obj):
        """
        Returns the numer of questions for the given quiz object.

        Args:
            obj (Quiz): The Quiz instance for which to count questions.

        Returns:
            int: The number of questions associated with the quiz.
        """
        return obj.questions.count()

class ModulShortSerializer(serializers.ModelSerializer):
    """
    Serializes a minimal representation of Modul objects, including only ID and name.
    Used for references and dropdowns.
    """
    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Modul
        fields = ['modulId', 'name']

class LernsetSerializer(serializers.ModelSerializer):
    """
    Serializes Lernset objects, including related quizzes and module information.
    Provides quiz count and supports nested quiz serialization for detailed views.
    """
    quizzes = QuizForLernsetSerializer(many=True, read_only=True)
    modul = ModulShortSerializer(read_only=True)
    quiz_count = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Lernset
        fields = ['id', 'title', 'description', 'created_at', 'modul', 'quizzes', 'quiz_count']

    def get_quiz_count(self, obj):
        """
        Returns the numer of quizzes for the given lernset object.

        Args:
            obj (Lernset): The Lernset instance for which to count quizzes.

        Returns:
            int: The number of quizzes associated with the lernset.
        """
        return obj.quizzes.count()

    def create(self, validated_data):
        # Need this for POST requests since we changed modul to read_only
        modul_id = self.initial_data.get('modul')
        modul = Modul.objects.get(modulId=modul_id)
        validated_data['modul'] = modul
        return super().create(validated_data)

class QuizSessionSerializer(serializers.ModelSerializer):
    """
    Serializes QuizSession objects, representing a user's session while solving a quiz.
    Includes timing, score, and mode information.
    """
    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = QuizSession
        fields = ['id', 'quiz', 'start_time', 'end_time', 'correct_answers', 'total_answers']

class FeedbackSerializer(serializers.ModelSerializer):
    """
    Serializes Feedback objects, representing user ratings and comments for quizzes.
    """
    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Feedback
        fields = ['id', 'quiz', 'rating', 'submitted_at']

class StudiengangSerializer(serializers.ModelSerializer):
    """
    Serializes Studiengang objects, representing fields of study.
    Includes related modules for overview and selection.
    """
    module = ModulShortSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Studiengang
        fields = ['id', 'name', 'description', 'modulux_url', 'module']

class ModulSerializer(serializers.ModelSerializer):
    """
    Serializes Modul objects, representing modules within a field of study.
    Includes all model fields.
    """
    lernset_count = serializers.IntegerField(source='lernsets.count', read_only=True)

    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Modul
        fields = '__all__'

class LernsetForModulSerializer(serializers.ModelSerializer):
    """
    Serializes Lernset objects for use within a Modul context.
    Provides quiz count for summary views.
    """
    quiz_count = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Lernset
        fields = ['id', 'title', 'description', 'created_at', 'quiz_count']

    def get_quiz_count(self, obj):
        """
        Returns the numer of quizzes for the given lernset object.

        Args:
            obj (Lernset): The Lernset instance for which to count quizzes.

        Returns:
            int: The number of quizzes associated with the lernset.
        """
        return obj.quizzes.count()

class ModulDetailSerializer(serializers.ModelSerializer):
    """
    Serializes detailed Modul objects, including all related lernsets.
    Used for detailed module views with nested lernset information.
    """
    lernsets = LernsetForModulSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class defining the model and fields to be serialized.
        """
        model = Modul
        fields = '__all__'
