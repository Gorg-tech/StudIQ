 # Integrationstests for quiz module
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.response import Response
from quizzes.models import AnswerOption, Question, QuizSession, Studiengang, Quiz, Lernset, Modul

from django.conf import settings
settings.ALLOWED_HOSTS = ['testserver']  # Ensure testserver is allowed
User = get_user_model()

class TestSearchView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.studiengang = Studiengang.objects.create(name="Informatik")

        self.user = User.objects.create_user(
            username="testuser",
            password="pass123",
            studiengang=self.studiengang
        )

        self.modul = Modul.objects.create(name="Modul 101", modulId="M101", credits=5)
        self.modul.studiengang.set([self.studiengang])  # Only here if Modul.studiengang is ManyToMany
        
        self.lernset = Lernset.objects.create(title="Sample Lernset", created_by=self.user, modul=self.modul)

        self.quiz = Quiz.objects.create(
            title="Test Quiz",
            description="Searchable quiz",
            created_by=self.user,
            lernset=self.lernset
        )

    def test_search_filters_by_quizzes(self):
        self.client.force_authenticate(self.user)

        response = self.client.get("/api/search/?q=test&filter=quizzes")

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data["quizzes"]), 1)
        self.assertEqual(len(response.data["lernsets"]), 0)

    