"""
Django App Configuration for accounts.

This file defines the django app configuration.
"""

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    """
    Default configuration for the app.
    Sets default field type and the name of the app.  
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
