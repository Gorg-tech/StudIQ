
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

class TestRegistration(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")

    def tearDown(self):
        return super().tearDown()

    def test_registration_with_missing_username(self):
        """Ensure that registration fails with missing username"""
        with self.assertRaises(IntegrityError):
            User.objects.create(username=None, password="testpass")

    def test_registration_with_missing_password(self):
        """Ensure that registration fails with missing password"""
        with self.assertRaises(IntegrityError):
            User.objects.create(username="testuser", password=None)

    def test_name_not_unique(self):
        """Ensure that registration fails when username is not unique"""
        with self.assertRaises(IntegrityError):
            User.objects.create(username="testuser", password="anotherpass")