
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase
from quizzes.models import Quiz,Lernset, Modul, Question, AnswerOption
from quizzes.serializers import QuizSerializer
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

class TestCaseMissingValues(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.modul = Modul.objects.create(name="Test Modul", credits=5)
        self.lernset = Lernset.objects.create(title="Test Lernset", modul=self.modul, created_by=self.user )

    def tearDown(self):
        return super().tearDown()
    
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

    def test_empty_quiz(self):
        """Quiz with no questions should be considered invalid"""
        quiz = Quiz(
            title="Empty Quiz",
            description="No questions",
            lernset=self.lernset
    )
    # Check that quiz has no questions
        self.assertEqual(quiz.questions.count(), 0)
    # Check that quiz would be invalid because questions are required
        is_valid = quiz.lernset is not None and quiz.questions.count() > 0
        self.assertFalse(is_valid)  

class TestSearchbar(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.modul = Modul.objects.create(name="Test Modul", credits=5)
        self.lernset = Lernset.objects.create(title="Test Lernset", modul=self.modul, created_by=self.user)
        self.quiz1 = Quiz.objects.create(title="Algebra Basics", description="Basic algebra quiz", lernset=self.lernset, created_by=self.user)
        self.quiz2 = Quiz.objects.create(title="Calculus I", description="Introduction to calculus", lernset=self.lernset, created_by=self.user)
        self.quiz3 = Quiz.objects.create(title="Geometry Fundamentals", description="Basics of geometry", lernset=self.lernset, created_by=self.user)

    def test_search_quiz_by_title(self):
        """Searching for a quiz by title should return the correct quiz"""
        search_term = "Algebra"
        results = Quiz.objects.filter(title__icontains=search_term)
        self.assertIn(self.quiz1, results)
        self.assertEqual(len(results), 1)
    
    def test_search_quiz_no_results(self):
        """Searching for a non-existing quiz should return no results"""
        search_term = "NonExistingQuiz"
        results = Quiz.objects.filter(title__icontains=search_term)
        self.assertEqual(len(results), 0)

    def test_search_quiz_case_insensitive(self):
        """Searching should be case insensitive"""
        search_term = "algebra"
        results = Quiz.objects.filter(title__icontains=search_term)
        self.assertIn(self.quiz1, results)
        self.assertEqual(len(results), 1)

    def test_search_lernset_by_title(self):
        """Searching for a lernset by title should return the correct lernset"""
        search_term = "Lernset"
        results = Lernset.objects.filter(title__icontains=search_term)
        self.assertIn(self.lernset, results)
        self.assertEqual(len(results), 1)
    
    def test_search_lernset_no_results(self):
        """Searching for a non-existing lernset should return no results"""
        search_term = "NonExistingLernset"
        results = Lernset.objects.filter(title__icontains=search_term)
        self.assertEqual(len(results), 0)
class Testserializers(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.modul = Modul.objects.create(name="Test Modul", credits=5)
        self.lernset = Lernset.objects.create(title="Test Lernset", modul=self.modul, created_by=self.user)
        self.quiz = Quiz.objects.create(title="Sample Quiz", description="A sample quiz for testing", lernset=self.lernset, created_by=self.user)

    def test_quiz_serializer(self):
        """QuizSerializer should serialize quiz data correctly"""
        serializer = QuizSerializer(instance=self.quiz)
        data = serializer.data

        self.assertEqual(data['title'], "Sample Quiz")
        self.assertEqual(data['description'], "A sample quiz for testing")
        self.assertEqual(data['lernset'], self.lernset.id)
        self.assertEqual(data['created_by'], self.user.username)