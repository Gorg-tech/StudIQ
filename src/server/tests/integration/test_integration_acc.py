# Integration tests for the accounts service
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from quizzes.models import Studiengang, Quiz, Lernset, Modul
from django.conf import settings
settings.ALLOWED_HOSTS = ['testserver']  # Ensure testserver is allowed
User = get_user_model()

class TestIntegrationAccounts(TestCase):
    def setUp(self):
        self.studiengang = Studiengang.objects.create(name="Informatik")
        
        self.user1 = User.objects.create(username="user1", studiengang=self.studiengang)
        self.user1.set_password("pass1")
        self.user1.save()

        self.user2 = User.objects.create(username="user2", studiengang=self.studiengang)
        self.user2.set_password("pass2")
        self.user2.save()
        
        self.client = APIClient()
        
        self.modul = Modul.objects.create(name="Modul 101", modulId="M101", credits=5)
        self.modul.studiengang.set([self.studiengang])  # Only here if Modul.studiengang is ManyToMany
        
        self.lernset = Lernset.objects.create(title="Sample Lernset", created_by=self.user1, modul=self.modul)

    def test_register_user_success(self):
        """Register a new user successfully if all required fields are provided"""
        print(self.studiengang.id)
        data = {"username": "newuser", "password": "Newpass1234#", "studiengang": "I41", "email": "newuser@example.com"}

        response = self.client.post("/api/auth/register/", data, format="json")
        print(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], "newuser")

    def test_register_user_invalid_fails(self):
        """Register fails when missing required fields"""
        data = {"username": ""}  # missing password
        response = self.client.post("/api/auth/register/", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)

    def test_login_invalid_credentials_fails(self):
        """Login fails with wrong password"""
        data = {"username": "user1", "password": "wrongpass"}
        response = self.client.post("/api/auth/login/", data, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.data)

    def test_valid_login_succeeds(self):
        """Login succeeds with correct credentials"""
        data = {"username": "user1", "password": "pass1"}
        response = self.client.post("/api/auth/login/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "user1")

    def test_valid_logout_succeeds(self):
        """Logout works after login"""
        self.client.login(username="user1", password="pass1")
        response = self.client.post("/api/auth/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("detail", response.data)

    def test_me_view_requires_authentication(self):
        """GET /me/ without login returns 401 or 403 - protected user endpoint"""
        response = self.client.get("/api/auth/me/")
        self.assertIn(response.status_code, [401, 403])

    def test_me_view_authenticated(self):
        """GET /me/ returns logged-in user data"""
        self.client.login(username="user1", password="pass1")
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "user1")

    def test_create_and_get_quiz_succeeds(self):
        """Create a quiz and fetch it"""
        self.client.login(username="user1", password="pass1")
        quiz_data = {
            "title": "Sample Quiz",
            "description": "A simple quiz",
            "lernset": self.lernset.id,
            "questions": [
                {
                    "text": "New Question 1",
                    "type": "SINGLE_CHOICE",
                    "_status": "new",
                    "answer_options": [
                        {"text": "New Answer 1", "is_correct": True, "_status": "new"},
                        {"text": "New Answer 2", "is_correct": False, "_status": "new"}
                    ]
                },
                {
                    "text": "New Question 2",
                    "type": "SINGLE_CHOICE",
                    "_status": "new",
                    "answer_options": [
                        {"text": "Answer 1", "is_correct": True, "_status": "new"},
                        {"text": "Answer 2", "is_correct": False, "_status": "new"}
                    ]
                },
                {
                    "text": "New Question 3",
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
        
        self.assertEqual(response.status_code, 201)
        quiz_id = response.data.get("id")
        self.assertIsNotNone(quiz_id)

        # Fetch quiz
        get_resp = self.client.get(f"/api/quizzes/{quiz_id}/")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.data["title"], "Sample Quiz")