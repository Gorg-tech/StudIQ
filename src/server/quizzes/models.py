import uuid
from django.db import models
from django.conf import settings

class Studiengang(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    modulux_url = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class Modul(models.Model):
    modulId = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    semester = models.IntegerField()
    description = models.TextField(blank=True)
    credits = models.IntegerField()
    modulux_url = models.URLField(blank=True)
    studiengang = models.ManyToManyField(Studiengang, related_name='module')
    
    def __str__(self):
        return self.name

class Lernset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE, related_name='lernsets')
    
    def __str__(self):
        return self.title

class QuestionType(models.TextChoices):
    MULTIPLE_CHOICE = 'MULTIPLE_CHOICE', 'Multiple Choice'
    ZUORDNUNG = 'ZUORDNUNG', 'Zuordnung'

class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating_score = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    estimated_duration = models.IntegerField(default=0)  # in minutes
    is_published = models.BooleanField(default=False)
    lernset = models.ForeignKey(Lernset, on_delete=models.CASCADE, related_name='quizzes')
    
    def __str__(self):
        return self.title

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    type = models.CharField(max_length=20, choices=QuestionType.choices)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    
    def __str__(self):
        return self.text[:50]

class AnswerOption(models.Model):
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_options')
    
    def __str__(self):
        return f"{self.text[:30]} ({'Correct' if self.is_correct else 'Incorrect'})"
