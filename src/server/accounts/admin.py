"""
Admin Configuration for account related objects.

This file registers all relevant models for the Django admin interface and
customizes their display, search, and filter options for superusers.
"""

"""
Admin Configuration for account related objects.

This file registers all relevant models for the Django admin interface and
customizes their display, search, and filter options for superusers.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudyDay, PendingFriendRequest

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.

    Extends Django's default UserAdmin to display app specific fields,
    such as role, iq_level, correct/wrong_answers, streak, solved_quizzes, and studiengang
    in the admin interface. Adjusts list display and fieldsets for better management
    of user profiles by superusers.
    """
    list_display = ('id', 'username', 'email', 'role', 'iq_score', 'streak')
    fieldsets = UserAdmin.fieldsets + (
        ('StudIQ Profile', {'fields': ('role', 'iq_score', 'correct_answers', 
                                      'streak_last_updated', 'wrong_answers', 'solved_quizzes',
                                      'studiengang', 'friends')}),
    )

@admin.register(StudyDay)
class StudyDayAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the StudyDay model.

    Adds StudyDays to the admin interface to create/delete StudyDays easily.
    """
    list_display = ('user', 'date')

@admin.register(PendingFriendRequest)
class PendingFriendRequestAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the PendingFriendRequest model.

    Adds PendingFriendRequests to the admin interface to manage friend requests.
    """
    list_display = ('from_user', 'to_user', 'sent_at')
