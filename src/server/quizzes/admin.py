from django.contrib import admin
from .models import (
    Studiengang, Modul, Lernset, Quiz, Question, AnswerOption,
    QuizAttempt, QuizSession, Feedback
)

@admin.register(Studiengang)
class StudiengangAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Modul)
class ModulAdmin(admin.ModelAdmin):
    list_display = ('modulId', 'name', 'credits')
    search_fields = ('name', 'modulId')
    # list_filter must be a tuple/list; ensure proper tuple syntax
    list_filter = ('studiengang',)

@admin.register(Lernset)
class LernsetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'created_at', 'modul')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'modul')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'is_public', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_public', 'created_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'type', 'quiz')
    list_filter = ('type', 'quiz')
    search_fields = ('text',)

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'is_correct', 'question')
    list_filter = ('is_correct', 'question')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quiz', 'correct_answers', 'wrong_answers', 'last_reviewed', 'attempts')
    list_filter = ('user', 'quiz')

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quiz', 'start_time', 'end_time')
    list_filter = ('user', 'quiz')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quiz', 'rating', 'submitted_at')
    list_filter = ('rating',)
