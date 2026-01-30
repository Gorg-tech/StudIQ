from django.test import TestCase
from quizzes.models import Quiz,Lernset, Modul, Question, AnswerOption
from quizzes.serializers import QuestionSerializer, QuizSerializer
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from accounts import serializers

User = get_user_model()

class TestSearchbar(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.modul = Modul.objects.create(name="Test Modul", credits=5)
        self.lernset = Lernset.objects.create(title="Test Lernset", modul=self.modul, created_by=self.user)
        self.quiz1 = Quiz.objects.create(title="Algebra Basics", description="Basic algebra quiz", lernset=self.lernset, created_by=self.user)
        self.quiz2 = Quiz.objects.create(title="Calculus I", description="Introduction to calculus", lernset=self.lernset, created_by=self.user)
        self.quiz3 = Quiz.objects.create(title="Geometry Fundamentals", description="Basics of geometry", lernset=self.lernset, created_by=self.user)

    def test_search_quiz_by_title_suceeds(self):
        """Searching for a quiz by title should return the correct quiz"""
        search_term = "Algebra"
        results = Quiz.objects.filter(title__icontains=search_term)
        self.assertIn(self.quiz1, results)
        self.assertEqual(len(results), 1)
    
    def test_search_nonexisting_quiz_fails(self):
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
