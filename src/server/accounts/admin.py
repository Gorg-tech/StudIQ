from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudyDay

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'role', 'iq_level', 'streak')  
    fieldsets = UserAdmin.fieldsets + (
        ('StudIQ Profile', {'fields': ('role', 'iq_level', 'correct_answers', 
                                      'wrong_answers', 'solved_quizzes', 
                                      'streak', 'studiengang')}),
    )

@admin.register(StudyDay)
class StudyDayAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')  # passt du an deine Felder an