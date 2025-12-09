"""
Database Model for account related objects.

This file defines account-related entites, their attribute fields and their relationships.
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from quizzes.models import Studiengang
class UserRole(models.TextChoices):
    """
    A datatype representing the role of the user.

    Options:
        STUDENT, MODERATOR, LECTURER
    """
    STUDENT = 'STUDENT', 'Student'
    MODERATOR = 'MODERATOR', 'Moderator'
    LECTURER = 'LECTURER', 'Lecturer'

class User(AbstractUser):
    """
    Represents a StudIQ account that has to be created to use StudIQ.

    Attributes:
        id, role, iq_level, streak, correct_answers,
        wrong_answers, solved_quizzes, registration_date, studiengang
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.STUDENT)
    iq_score = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    solved_quizzes = models.IntegerField(default=0)
    registration_date = models.DateField(auto_now_add=True)
    # last_login is already part of AbstractUser

    # Will be linked to Studiengang later
    studiengang = models.ForeignKey(Studiengang, on_delete=models.SET_NULL, null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=True)

    def __str__(self):
        return self.username

class StudyDay(models.Model):
    """
    Represents a day at which the user had studied.

    Attributes:
        user, date
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_days')
    date = models.DateField()

    class Meta:
        """
        Defines primary key behaviour for user,date and orders by date descending.
        """
        unique_together = ('user', 'date')  # Entry per user per day should be unique
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class PendingFriendRequest(models.Model):
    """
    Represents a pending friend request between two users.

    Attributes:
        from_user, to_user, sent_at
    """
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='received_friend_requests')
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Defines primary key behaviour for from_user,to_user pairs.
        """
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"Friend request from {self.from_user.username} to {self.to_user.username}"
