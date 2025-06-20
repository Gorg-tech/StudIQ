from django.contrib import admin
from .models import (
    Studiengang, Modul, Lernset, Quiz, Question, AnswerOption,
    QuizProgress, Achievement, QuizSession, Feedback, UserAchievement
)

@admin.register(Studiengang)
class StudiengangAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Modul)
class ModulAdmin(admin.ModelAdmin):
    list_display = ('modulId', 'name', 'semester', 'credits')
    search_fields = ('name', 'modulId')
    list_filter = ('semester', 'studiengang')

@admin.register(Lernset)
class LernsetAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'modul')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'modul')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    # Change is_published to is_public
    list_display = ('title', 'created_by', 'is_public', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_public', 'created_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'type', 'quiz')
    list_filter = ('type', 'quiz')
    search_fields = ('text',)

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'question')
    list_filter = ('is_correct', 'question')

@admin.register(QuizProgress)
class QuizProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'correct_answers', 'wrong_answers', 'last_reviewed', 'strength_score')
    list_filter = ('user', 'quiz')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'unlock_criteria')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'unlocked_at')
    list_filter = ('achievement', 'unlocked_at')

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'start_time', 'end_time', 'score', 'mode')
    list_filter = ('mode', 'user')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'rating', 'submitted_at')
    list_filter = ('rating',)
