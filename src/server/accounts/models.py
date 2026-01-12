"""
Database Model for account related objects.

This file defines account-related entites, their attribute fields and their relationships.
"""

import uuid
from datetime import timedelta, date
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
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
    _streak = models.IntegerField(default=0, db_column='streak')  # Private field, accessed via property
    streak_last_updated = models.DateField(null=True, blank=True)  # Tracks last calculation date
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    solved_quizzes = models.IntegerField(default=0)
    registration_date = models.DateField(auto_now_add=True)
    # last_login is already part of AbstractUser

    # Will be linked to Studiengang later
    studiengang = models.ForeignKey(Studiengang, on_delete=models.SET_NULL, null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=True)

    @property
    def streak(self):
        """
        Get the current study streak, recalculating only if needed (not done today).
        Uses lazy evaluation with daily caching to ensure accuracy while minimizing DB writes.
        
        Returns:
            int: The current streak count.
        """
        today = date.today()
        
        # Only recalculate if not done today
        if self.streak_last_updated != today:
            days = list(self.study_days.values_list('date', flat=True).order_by('-date'))
            streak = 0
            last_day = today

            for d in days:
                if d > last_day:
                    continue
                if last_day - d in [timedelta(days=0), timedelta(days=1)]:
                    streak += 1
                    last_day = d
                else:
                    break

            # Only save if streak changed or we haven't checked today
            if self._streak != streak or self.streak_last_updated != today:
                self._streak = streak
                self.streak_last_updated = today
                self.save(update_fields=['_streak', 'streak_last_updated'])

        return self._streak

    @streak.setter
    def streak(self, value):
        """Allow setting streak directly if needed (e.g., during migration or reset)."""
        self._streak = value

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


# Signal handlers for streak cache invalidation
@receiver(post_save, sender=StudyDay)
def invalidate_streak_on_study_day_created(sender, instance, created, **kwargs):
    """
    Invalidate the cached streak for the specific user when a StudyDay is created.
    Only invalidates the streak for the user in this StudyDay, not all users.
    """
    if created:
        # Only invalidate the streak for the user in this StudyDay
        instance.user.streak_last_updated = None
        # Access streak property to trigger recalculation
        _ = instance.user.streak


@receiver(post_delete, sender=StudyDay)
def invalidate_streak_on_study_day_deleted(sender, instance, **kwargs):
    """
    Invalidate the cached streak for the specific user when a StudyDay is deleted.
    Only invalidates the streak for the user in this StudyDay, not all users.
    """
    # Only invalidate the streak for the user in this StudyDay
    instance.user.streak_last_updated = None
    # Access streak property to trigger recalculation
    _ = instance.user.streak
