import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from quizzes.models import Studiengang

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
    studiengang = models.ForeignKey(Studiengang, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.username