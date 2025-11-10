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

    def test_quiz_without_lernset_raises_error(self):
        """
        Ensure creating a Quiz without a Lernset raises an IntegrityError
        because lernset is a required ForeignKey.
        """
        with self.assertRaises(IntegrityError):
            Quiz.objects.create(
                title="Orphan Quiz",
                description="No Lernset associated"
                # lernset is missing
            )

    def test_missing_quiz_name_model(self):
        """Quiz without title raises IntegrityError"""
        with self.assertRaises(IntegrityError):
            Quiz.objects.create(
                title=None,
                description="No title",
                lernset=self.lernset
            )
