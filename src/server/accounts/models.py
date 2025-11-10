import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    STUDENT = 'STUDENT', 'Student'
    MODERATOR = 'MODERATOR', 'Moderator'
    LECTURER = 'LECTURER', 'Lecturer'

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.STUDENT)
    iq_level = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    solved_quizzes = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    registration_date = models.DateField(auto_now_add=True)
    # last_login is already part of AbstractUser
    
    # Will be linked to Studiengang later
    studiengang = models.CharField(max_length=100, null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.username
    
class StudyDay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_days')
    date = models.DateField()
    
    class Meta:
        unique_together = ('user', 'date')  # Entry per user per day should be unique
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"