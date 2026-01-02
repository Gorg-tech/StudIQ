"""
Database Model for quiz related objects.

This file defines quiz-related entites, their attribute fields and their relationships.
"""

import uuid
from django.db import models
from django.conf import settings

class Studiengang(models.Model):
    """
    Represents a field of study, such as computer science.

    Attributes:
        id, name, description, created_at, modulux_url
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    modulux_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Modul(models.Model):
    """
    Represents a module, such as math.

    Attributes:
        modulId, name, semesters, examinations, turnus, languages,
        credits, modulux_url, dozent_name, dozent_email, studiengang
    """
    modulId = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    examinations = models.TextField(blank=True)
    turnus = models.CharField(max_length=50, blank=True)
    languages = models.JSONField(blank=True, default=list)
    credits = models.IntegerField()
    modulux_url = models.URLField(blank=True)
    dozent_name = models.CharField(max_length=100, blank=True)
    dozent_email = models.EmailField(blank=True)
    studiengang = models.ManyToManyField(Studiengang, related_name='module')

    def __str__(self):
        return self.name

class Lernset(models.Model):
    """
    Represents a subject area of a specific module and a supercategory of a set of quizzes.

    Attributes:
        id, title, description, created_at, created_by, modul
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE, related_name='lernsets')

    def __str__(self):
        return self.title

class QuestionType(models.TextChoices):
    """
    A datatype representing different types of questions.

    Choices:
        MULTIPLE_CHOICE, SINGLE_CHOICE, ZUORDNUNG
    """
    MULTIPLE_CHOICE = 'MULTIPLE_CHOICE', 'Multiple Choice'
    SINGLE_CHOICE = 'SINGLE_CHOICE', 'Single Choice'
    ZUORDNUNG = 'ZUORDNUNG', 'Zuordnung'

class Quiz(models.Model):
    """
    Represents a quiz that the user can solve.

    Attributes:
        id, title, description, created_at, created_by, rating_score, rating_count, is_public,
        lernset, last_content_update, total_attempts, completion_rate, avg_score, avg_time_spent,
        difficulty_rating, most_missed_question_id, last_stats_update
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)  
    lernset = models.ForeignKey(Lernset, on_delete=models.CASCADE, related_name='quizzes')

    last_content_update = models.DateTimeField(auto_now=True)
    total_attempts = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0.0)
    avg_score = models.FloatField(default=0.0)
    avg_time_spent = models.IntegerField(default=0)  # in seconds
    difficulty_rating = models.FloatField(default=0.0)
    most_missed_question_id = models.UUIDField(null=True, blank=True)
    last_stats_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    """
    Represents a single question of a quiz.

    Attributes:
        id, text, type, quiz
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    type = models.CharField(max_length=20, choices=QuestionType.choices)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text[:50]

class AnswerOption(models.Model):
    """
    Represents a single option of a question.

    Attributes:
        text, is_correct, question
    """
    # Führt zu Internal Server Error
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_options')

    def __str__(self):
        return f"{self.text[:30]} ({'Correct' if self.is_correct else 'Incorrect'})"

class QuizSession(models.Model):
    """
    Represents a single attempt/session of a user on a quiz.

    Attributes:
        user, quiz, start_time, end_time, correct_answers, total_answers
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='quiz_sessions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    correct_answers = models.IntegerField(default=0)
    total_answers = models.IntegerField(default=0)

    class Meta:
        """
        Defines unique active session (end_time=NULL) constraint per (user,quiz).
        """
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'quiz'],
                condition=models.Q(end_time__isnull=True),
                name='unique_active_session_per_user_quiz'
            )
        ]

    def __str__(self):
        return f"{self.id}"

class Feedback(models.Model):
    """
    Represents feedback on a quiz from a user including a comment and a rating.

    Attributes:
        user, quiz, rating, comment, submitted_at
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='feedback')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.rating}/5"
