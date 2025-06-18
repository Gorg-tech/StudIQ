import uuid
from django.db import models

class UserRole(models.TextChoices):
    STUDENT = 'STUDENT', 'Student'
    MODERATOR = 'MODERATOR', 'Moderator'
    LECTURER = 'LECTURER', 'Lecturer'

class QuizType(models.TextChoices):
    MULTIPLE_CHOICE = 'MULTIPLE_CHOICE', 'Multiple Choice'
    FREITEXT = 'FREITEXT', 'Freitext'
    ZUORDNUNG = 'ZUORDNUNG', 'Zuordnung'

class DifficultyLevel(models.TextChoices):
    EASY = 'EASY', 'Easy'
    MEDIUM = 'MEDIUM', 'Medium'
    HARD = 'HARD', 'Hard'

class QuizMode(models.TextChoices):
    PRACTICE = 'PRACTICE', 'Practice'
    SIMULATION = 'SIMULATION', 'Simulation'
    FLASHCARDS = 'FLASHCARDS', 'Flashcards'
    CHALLENGE = 'CHALLENGE', 'Challenge'

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=UserRole.choices)
    registrationDate = models.DateField(auto_now_add=True)

class Modul(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    semester = models.CharField(max_length=50)
    description = models.TextField()

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    modul = models.ForeignKey(Modul, related_name="topics", on_delete=models.CASCADE)

class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    type = models.CharField(max_length=20, choices=QuizType.choices)
    difficulty = models.CharField(max_length=10, choices=DifficultyLevel.choices)
    explanation = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    rating_score = models.IntegerField(default=0)
    topic = models.ForeignKey(Topic, related_name="quizzes", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="quizzes", on_delete=models.CASCADE)

class AnswerOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    isCorrect = models.BooleanField()
    quiz = models.ForeignKey(Quiz, related_name="answer_options", on_delete=models.CASCADE)

class QuizProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="quiz_progress", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name="quiz_progress", on_delete=models.CASCADE)
    correctAnswers = models.IntegerField(default=0)
    wrongAnswers = models.IntegerField(default=0)
    lastReviewed = models.DateTimeField(null=True, blank=True)
    strengthScore = models.FloatField(default=0.0)

class LearningHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, related_name="learning_history", on_delete=models.CASCADE)
    iq_level = models.IntegerField(default=0)
    correctAnswers = models.IntegerField(default=0)
    wrongAnswers = models.IntegerField(default=0)
    solvedQuizzes = models.IntegerField(default=0)
    login_streak = models.IntegerField(default=0)

class Badge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()

class QuizSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    mode = models.CharField(max_length=15, choices=QuizMode.choices)

class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.IntegerField()
    comment = models.TextField()
    submittedAt = models.DateField(auto_now_add=True)

class StudyGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    createdAt = models.DateField(auto_now_add=True)