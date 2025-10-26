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
    SINGLE_CHOICE = 'SINGLE_CHOICE', 'Single Choice'
    ZUORDNUNG = 'ZUORDNUNG', 'Zuordnung'

class Quiz(models.Model):
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    type = models.CharField(max_length=20, choices=QuestionType.choices)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    
    def __str__(self):
        return self.text[:50]

class AnswerOption(models.Model):
    # Führt zu Internal Server Error
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_options')
    
    def __str__(self):
        return f"{self.text[:30]} ({'Correct' if self.is_correct else 'Incorrect'})"

class QuizProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_progress')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='progress')
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(auto_now=True)
    strength_score = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ('user', 'quiz')
        
    def __str__(self):
        return f"{self.user.username}'s progress on {self.quiz.title}"

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    unlock_criteria = models.CharField(max_length=255)
    icon_url = models.URLField()
    
    # Many-to-many relationship with User through UserAchievement
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserAchievement')
    
    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')

class QuizMode(models.TextChoices):
    PRACTICE = 'PRACTICE', 'Practice'
    SIMULATION = 'SIMULATION', 'Simulation'
    FLASHCARDS = 'FLASHCARDS', 'Flashcards'

class QuizSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_sessions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    mode = models.CharField(max_length=20, choices=QuizMode.choices, default=QuizMode.PRACTICE)
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.rating}/5"