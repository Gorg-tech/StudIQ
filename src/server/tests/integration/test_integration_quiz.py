 # Integrationstests for quiz module
from urllib import response
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
        """Test that the 'created_by' field is set automatically on quiz creation."""
        self.client.force_authenticate(self.creator)

        quiz_data = {
        "title": "New Quiz",
        "description": "Test quiz",
        "lernset": self.lernset.id,
        "questions": [
            {
                "text": "Question 1",
                "type": "SINGLE_CHOICE",
                "_status": "new",
                "answer_options": [
                    {"text": "Answer 1", "is_correct": True, "_status": "new"},
                    {"text": "Answer 2", "is_correct": False, "_status": "new"}
                ]
            },
            {
                "text": "Question 2",
                "type": "SINGLE_CHOICE",
                "_status": "new",
                "answer_options": [
                    {"text": "Answer 1", "is_correct": True, "_status": "new"},
                    {"text": "Answer 2", "is_correct": False, "_status": "new"}
                ]
            },
            {
                "text": "Question 3",
                "type": "SINGLE_CHOICE",
                "_status": "new",
                "answer_options": [
                    {"text": "Answer 1", "is_correct": True, "_status": "new"},
                    {"text": "Answer 2", "is_correct": False, "_status": "new"}
                ]
            }
        ]
        }

        response = self.client.post("/api/quizzes/", quiz_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        quiz = Quiz.objects.get(id=response.data["id"])
        self.assertEqual(quiz.created_by, self.creator)

    def test_only_creator_can_delete_quiz(self):
        """Test that only the creator of a quiz can delete it."""
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
        """Test that a new quiz session can be created successfully."""
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


    def test_answer_correct_increases_correct_answers_successful(self):
        """Test that answering a question correctly increases the correct answer count in the session."""
        self.client.force_authenticate(self.creator)

        question = Question.objects.create(
            quiz=self.quiz,
            text="2+2?",
            type="SINGLE"
        )
        correct = AnswerOption.objects.create(question=question, text="4", is_correct=True)
        wrong = AnswerOption.objects.create(question=question, text="5", is_correct=False)

        self.client.post(f"/api/quizzes/{self.quiz.id}/start/")

        response = self.client.post(
            f"/api/quizzes/{self.quiz.id}/answer/",
            {
                "question_id": str(question.id),
                "selected_option_ids": [str(correct.id)]
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_correct"])

    def test_answer_wrong_is_marked_incorrect_successful(self):
        """Test that answering a question incorrectly is marked as incorrect."""
        self.client.force_authenticate(self.creator)

        question = Question.objects.create(
            quiz=self.quiz,
            text="Capital of Germany?",
            type="SINGLE"
        )
        AnswerOption.objects.create(question=question, text="Berlin", is_correct=True)
        wrong = AnswerOption.objects.create(question=question, text="Paris", is_correct=False)

        self.client.post(f"/api/quizzes/{self.quiz.id}/start/")

        response = self.client.post(
            f"/api/quizzes/{self.quiz.id}/answer/",
            {
                "question_id": str(question.id),
                "selected_option_ids": [str(wrong.id)]
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_correct"])

    def test_complete_quiz_updates_iq_and_ends_session(self):
        """Test that completing a quiz updates the user's IQ score and ends the session."""
        self.client.force_authenticate(self.creator)

        question = Question.objects.create(
            quiz=self.quiz,
            text="1+1?",
            type="SINGLE"
        )
        correct = AnswerOption.objects.create(question=question, text="2", is_correct=True)

        self.client.post(f"/api/quizzes/{self.quiz.id}/start/")
        self.client.post(
            f"/api/quizzes/{self.quiz.id}/answer/",
            {
                "question_id": str(question.id),
                "selected_option_ids": [str(correct.id)]
            },
            format="json"
        )

        prev_iq = self.creator.iq_score
        response = self.client.post(f"/api/quizzes/{self.quiz.id}/complete/")

        self.creator.refresh_from_db()
        session = QuizSession.objects.get(user=self.creator, quiz=self.quiz)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(session.end_time)
        self.assertGreater(self.creator.iq_score, prev_iq)

    def test_leaderboard_returns_users(self):
        """Test that the leaderboard endpoint returns a list of users."""
        self.client.force_authenticate(self.creator)

        response = self.client.get("/api/leaderboard/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.data)
        self.assertGreaterEqual(len(response.data["users"]), 1)

    def test_suggested_quizzes_for_studiengang(self):
        """Test that suggested quizzes for a user's studiengang are returned."""
        self.client.force_authenticate(self.creator)

        response = self.client.get("/api/suggested-quizzes/")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data), 3)