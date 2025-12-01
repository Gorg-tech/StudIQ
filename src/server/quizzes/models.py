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
    semester = models.IntegerField()
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
    rating_score = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
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

class QuizProgress(models.Model):
    """
    Represents the statistics of a user on a quiz (including ALL attempts)

    Attributes:
        user, quiz, correct_answers, wrong_answers, last_reviewed, strength_score, attempts
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                             related_name='quiz_progress')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='progress')
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(auto_now=True)
    strength_score = models.FloatField(default=0.0)
    attempts = models.IntegerField(default=0)

    class Meta:
        """
        Defines primary key behaviour for tuple user,quiz.
        """
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f"{self.user.username}'s progress on {self.quiz.title}"

class Achievement(models.Model):
    """
    Represents an achievement that can be unlocked by the user by fulfilling the unlock criteria.

    Attributes:
        name, description, unlock_criteria, icon_url
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    unlock_criteria = models.CharField(max_length=255)
    icon_url = models.URLField()

    # Many-to-many relationship with User through UserAchievement
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserAchievement')

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    """
    Represents an unlocked achievement for a user.

    Attributes:
        user, achievement, unlocked_at
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Defines primary key behaviour for user,achievement.
        """
        unique_together = ('user', 'achievement')

class QuizMode(models.TextChoices):
    """
    A datatype representing the mode in which a quiz has been solved. 
    """
    PRACTICE = 'PRACTICE', 'Practice'
    SIMULATION = 'SIMULATION', 'Simulation'
    FLASHCARDS = 'FLASHCARDS', 'Flashcards'

class QuizSession(models.Model):
    """
    Represents a temporary session while the user is solving a quiz.

    Attributes:
        user, quiz, start_time, end_time, score, mode
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='quiz_sessions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    mode = models.CharField(max_length=20, choices=QuizMode.choices, default=QuizMode.PRACTICE)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - \
            {self.start_time.strftime('%Y-%m-%d %H:%M')}"

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
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.rating}/5"
