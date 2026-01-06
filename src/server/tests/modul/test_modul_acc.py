from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from accounts.serializers import RegisterSerializer, LoginSerializer, FriendRequestSerializer
from accounts.models import FriendRequest
from django.contrib.auth import authenticate

User = get_user_model()

class TestAccounts(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass12345!?")

    def test_creating_new_valid_user_suceeds(self):
        data={
            "username": "newuser",
            "password": "StrongPassword123!#",
            "studiengang" : "I41"
        }

        serializer=RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user=serializer.save()

    def test_login_with_valid_credentials_succeeds(self):
        data={ 
            "username": self.user.username,
            "password": "testpass12345!?"
            }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_login_with_invalid_credentials_fails(self):
        data={ 
            "username": self.user.username,
            "password": "wrongpassword"
            }
        
        serializer = LoginSerializer(data=data)
        user=authenticate(username=data["username"], password=data["password"])
        self.assertIsNone(user)
        
    def test_missing_stdiengang_fails(self):
        data={
            "username": "anotheruser",
            "password": "anotherpass"
        }
        serializer=RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_creating_user_with_existing_username_fails(self):

        data={
            "username": self.user.username,
            "password": self.user.password,
            "studiengang" : "Informatik"
        }

        serializer=RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_warning_on_weak_password(self):
        data={
            "username": "weakuser",
            "password": "123",
            "studiengang" : "Informatik"
        }

        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)


    def test_friendrequest_to_unknown_user_fails(self):
        data={
            "from_user": self.user.username,
            "to_user": "unknownuser"
        }

        serializer=FriendRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

  