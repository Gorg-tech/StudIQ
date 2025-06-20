from django.contrib import admin
from .models import (
    Studiengang, Modul, Lernset, Quiz, Question, AnswerOption
)

@admin.register(Studiengang)
class StudiengangAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Modul)
class ModulAdmin(admin.ModelAdmin):
    list_display = ('modulId', 'name', 'semester', 'credits')
    list_filter = ('semester',)
    search_fields = ('name',)

@admin.register(Lernset)
class LernsetAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'is_published', 'rating_score')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title',)

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'type', 'quiz')
    list_filter = ('type',)
    search_fields = ('text',)
    inlines = [AnswerOptionInline]
