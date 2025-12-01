"""
Admin Configuration for quiz related objects.

This file registers all relevant models for the Django admin interface and
customizes their display, search, and filter options for superusers.
"""

from django.contrib import admin
from .models import (
    Studiengang, Modul, Lernset, Quiz, Question, AnswerOption,
    QuizProgress, Achievement, QuizSession, Feedback, UserAchievement
)

@admin.register(Studiengang)
class StudiengangAdmin(admin.ModelAdmin):
    """
    Admin interface for Studiengang model.
    Displays basic information and allows searching by name.
    """
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Modul)
class ModulAdmin(admin.ModelAdmin):
    """
    Admin interface for Modul model.
    Shows module details, allows filtering by semester and study program.
    """
    list_display = ('modulId', 'name', 'semester', 'credits')
    search_fields = ('name', 'modulId')
    list_filter = ('semester', 'studiengang')

@admin.register(Lernset)
class LernsetAdmin(admin.ModelAdmin):
    """
    Admin interface for Lernset model.
    Displays Lernset details, creator, and allows filtering by module and creation date.
    """
    list_display = ('id', 'title', 'created_by', 'created_at', 'modul')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'modul')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """
    Admin interface for Quiz model.
    Shows quiz details, creator, and allows filtering by public status and creation date.
    """
    list_display = ('id', 'title', 'created_by', 'is_public', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_public', 'created_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin interface for Question model.
    Displays question text, type, and related quiz.
    """
    list_display = ('id', 'text', 'type', 'quiz')
    list_filter = ('type', 'quiz')
    search_fields = ('text',)

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    """
    Admin interface for AnswerOption model.
    Shows answer text, correctness, and related question.
    """
    list_display = ('id', 'text', 'is_correct', 'question')
    list_filter = ('is_correct', 'question')

@admin.register(QuizProgress)
class QuizProgressAdmin(admin.ModelAdmin):
    """
    Admin interface for QuizProgress model.
    Displays user progress on quizzes, including correct/wrong answers and review date.
    """
    list_display = ('id', 'user', 'quiz', 'correct_answers', 'wrong_answers', 'last_reviewed', 'strength_score')
    list_filter = ('user', 'quiz')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """
    Admin interface for Achievement model.
    Shows achievement details and unlock criteria.
    """
    list_display = ('id', 'name', 'description', 'unlock_criteria')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """
    Admin interface for UserAchievement model.
    Displays which user unlocked which achievement and when.
    """
    list_display = ('id', 'user', 'achievement', 'unlocked_at')
    list_filter = ('achievement', 'unlocked_at')

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    """
    Admin interface for QuizSession model.
    Shows quiz session details, user, score, and mode.
    """
    list_display = ('id', 'user', 'quiz', 'start_time', 'end_time', 'score', 'mode')
    list_filter = ('mode', 'user')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Admin interface for Feedback model.
    Displays feedback details, user, quiz, rating, and submission date.
    """
    list_display = ('id', 'user', 'quiz', 'rating', 'submitted_at')
    list_filter = ('rating',)
