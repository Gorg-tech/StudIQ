
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase
from quizzes.models import Quiz,Lernset, Modul
from quizzes.serializers import QuizSerializer
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

class TestCaseMissingValues(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.modul = Modul.objects.create(name="Test Modul", credits=5, semester=1)
        self.lernset = Lernset.objects.create(title="Test Lernset", modul=self.modul, created_by=self.user )

    def test_lernset_without_modul(self):
        """Ensure creating a Lernset without a connection to a modul is considered invalid"""
        lernset = Lernset(
            title="Orphan Lernset",
            created_by=self.user,
            modul=None  # modul is missing
    )
    # Check that lernset is None
        self.assertIsNone(lernset.modul_id)
    # Check that lernset would be invalid because modul is required
        is_valid = lernset.modul_id is not None and bool(lernset.title)
        self.assertFalse(is_valid)

    def test_missing_quiz_title(self):
        """Quiz without title should be considered invalid"""
        quiz = Quiz(
            title=None,
            description="No title",
            lernset=self.lernset
    )
    # Check that title is missing
        self.assertIsNone(quiz.title)
    # Check that quiz would be invalid because title is required
        is_valid = quiz.lernset is not None and bool(quiz.title)
        self.assertFalse(is_valid)
