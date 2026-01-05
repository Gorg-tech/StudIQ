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

class TestIntegrationQuiz(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.studiengang = Studiengang.objects.create(name="Informatik")
        self.modul = Modul.objects.create(name="Modul 101", modulId="M101", credits=5)

        self.creator = User.objects.create_user(
            username="creator",
            password="pass123",
            studiengang=self.studiengang
        )

        self.other_user = User.objects.create_user(
            username="other",
            password="pass123",
            studiengang=self.studiengang
        )

        self.moderator = User.objects.create_user(
            username="moderator",
            password="pass123",
            role="MODERATOR",
            studiengang=self.studiengang
        )
        self.lernset = Lernset.objects.create(title="Sample Lernset", created_by=self.creator, modul=self.modul)

        self.quiz = Quiz.objects.create(
            title="Sample Quiz",
            description="A sample quiz",
            created_by=self.creator,
            lernset = self.lernset
        )

        self.url = f"/api/quizzes/{self.quiz.id}/"

    def test_update_quiz_unauthenticated_user_forbidden(self):

        """Update quiz details as an unauthenticated user throws error"""
        response = self.client.put(
        self.url,
        {"title": "Hacked"},
        format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, "Sample Quiz")# Forbidden for unauthenticated users

    def test_quiz_create_sets_created_by_automatically(self):
        self.client.force_authenticate(self.creator)

        response = self.client.post(
        "/api/quizzes/",
        {
            "title": "New Quiz",
            "description": "Test quiz",
            "lernset": self.lernset.id
        },
        format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        quiz = Quiz.objects.get(id=response.data["id"])
        self.assertEqual(quiz.created_by, self.creator)

    def test_only_creator_can_delete_quiz(self):
        quiz = Quiz.objects.create(
            title="Test",
            created_by=self.creator,
            lernset=self.lernset
        )
        url = f"/api/quizzes/{quiz.id}/"

        self.client.force_authenticate(self.other_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_create_new_session_succeeds(self):
        self.client.force_authenticate(self.creator)
        
        question = Question.objects.create(
        quiz=self.quiz,
        text="What is 2 + 2?",
        type="SINGLE"
        )

        AnswerOption.objects.create(
            question=question,
            text="4",
            is_correct=True
        )

        response = self.client.post(
            f"/api/quizzes/{self.quiz.id}/start/",
            {},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    

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
