"""
Django App Configuration for quizzes.

This file defines the django app configuration.
"""

from django.apps import AppConfig

class QuizzesConfig(AppConfig):
    """
    Default configuration for the app.
    Sets default field type and the name of the app.  
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quizzes'
