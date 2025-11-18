from rest_framework import serializers
from .models import Quiz, Question, AnswerOption, Lernset, QuizProgress, Achievement, QuizSession, Feedback, Studiengang, Modul

class AnswerOptionSerializer(serializers.ModelSerializer):
    _status = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'is_correct', '_status']

class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True)
    quiz = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.UUIDField(required=False)
    _status = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'answer_options', 'quiz', '_status']

class QuizSerializer(serializers.ModelSerializer):
    lernset_title = serializers.CharField(source='lernset.title', read_only=True)
    questions = QuestionSerializer(many=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
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
        

    def update(self, instance, validated_data):
        print("--- Starting Quiz Update ---")
        print(f"Quiz ID: {instance.id}")
        print(f"Incoming validated data: {validated_data}")

        questions_data = validated_data.pop('questions', [])
        # Update Quiz fields
        for attr, value in validated_data.items():
            print(f"Updating quiz attribute '{attr}' to '{value}'")
            setattr(instance, attr, value)
        instance.save()
        
        # Verarbeite Questions basierend auf ihrem Status
        print("\n--- Processing Questions ---")
        for question_data in questions_data:
            status = question_data.pop('_status', None)
            question_id = question_data.get('id') # Use .get() to avoid removing it
            answer_options_data = question_data.pop('answer_options', [])
            
            print(f"\nProcessing Question with ID: {question_id}, Status: {status}")
            print(f"Question data: {question_data}")

            if status == 'new':
                print("  Action: Creating new question.")
                # Remove temporary frontend ID
                question_data.pop('id', None)
                question = Question.objects.create(quiz=instance, **question_data)
                for answer_data in answer_options_data:
                    answer_data.pop('id', None)
                    AnswerOption.objects.create(question=question, **answer_data)
                    
            elif status == 'edited' and question_id:
                print("  Action: Editing existing question.")
                question = Question.objects.get(id=question_id, quiz=instance)
                question.text = question_data.get('text', question.text)
                question.type = question_data.get('type', question.type)
                question.save()
                print(f"  Saved changes for question text: {question.text}")
                
                # Update or create AnswerOptions
                existing_answer_ids = set(question.answer_options.values_list('id', flat=True))
                received_answer_ids = set()

                print("  --- Processing Answer Options ---")
                for answer_data in answer_options_data:
                    answer_id = answer_data.get('id')
                    answer_status = answer_data.pop('_status', 'unchanged')
                    print(f"    Answer ID: {answer_id}, Status: {answer_status}, Data: {answer_data}")

                    if answer_status == 'new':
                        print("      Action: Creating new answer.")
                        answer_data.pop('id', None)
                        AnswerOption.objects.create(question=question, **answer_data)
                    elif answer_status == 'edited' and answer_id in existing_answer_ids:
                        print("      Action: Editing existing answer.")
                        answer_instance = AnswerOption.objects.get(id=answer_id)
                        answer_instance.text = answer_data.get('text', answer_instance.text)
                        answer_instance.is_correct = answer_data.get('is_correct', answer_instance.is_correct)
                        answer_instance.save()
                        received_answer_ids.add(answer_id)
                    elif answer_status == 'deleted' and answer_id in existing_answer_ids:
                        print("      Action: Deleting answer.")
                        AnswerOption.objects.filter(id=answer_id).delete()
                    elif answer_id in existing_answer_ids:
                         print("      Action: Answer unchanged.")
                         received_answer_ids.add(answer_id)

            elif status == 'deleted' and question_id:
                print(f"  Action: Deleting question with ID {question_id}")
                Question.objects.filter(id=question_id, quiz=instance).delete()
            else:
                print(f"  Action: No status or unknown status '{status}', skipping question modification.")
        
        print("\n--- Finished Quiz Update ---")
        return instance

class QuizForLernsetSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    creator_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
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
                 'last_reviewed', 'strength_score', 'attempts']
        
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
    module = ModulShortSerializer(many=True, read_only=True)
    
    class Meta:
        model = Studiengang
        fields = ['id', 'name', 'description', 'modulux_url', 'module']

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
