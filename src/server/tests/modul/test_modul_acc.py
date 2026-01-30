import uuid
from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from accounts.serializers import RegisterSerializer, LoginSerializer, PendingFriendRequestSerializer
from accounts.models import PendingFriendRequest, StudyDay
from django.contrib.auth import authenticate
from datetime import date
from accounts.views import get_user_rank

User = get_user_model()

class TestAccounts(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass12345!?")

    def test_creating_new_valid_user_suceeds(self):
        """Creating a new user with valid data succeeds"""
        data={
            "username": "newuser",
            "password": "StrongPassword123!#",
            "studiengang" : "I41"
        }

        serializer=RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user=serializer.save()

    def test_login_with_valid_credentials_succeeds(self):
        """Login with correct credentials succeeds"""
        data={ 
            "username": self.user.username,
            "password": "testpass12345!?"
            }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_login_with_invalid_credentials_fails(self):
        """Login with wrong password fails"""
        data={ 
            "username": self.user.username,
            "password": "wrongpassword"
            }
        
        serializer = LoginSerializer(data=data)
        user=authenticate(username=data["username"], password=data["password"])
        self.assertIsNone(user)
        
    def test_missing_stdiengang_fails(self):
        """Creating a new user without studiengang fails"""
        data={
            "username": "anotheruser",
            "password": "anotherpass"
        }
        serializer=RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_creating_user_with_existing_username_fails(self):
        """Creating a user with an existing username fails"""

        data={
            "username": self.user.username,
            "password": self.user.password,
            "studiengang" : "Informatik"
        }

        serializer=RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_warning_on_weak_password(self):
        """Creating a user with a weak password fails validation"""
        data={
            "username": "weakuser",
            "password": "123",
            "studiengang" : "Informatik"
        }

        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_friendrequest_unique_constraint(self):
        """Creating duplicate friend requests fails due to unique constraint"""
        PendingFriendRequest.objects.all().delete()
        user2 = User.objects.create(username="user2")
        PendingFriendRequest.objects.create(from_user=self.user, to_user=user2)

        with self.assertRaises(IntegrityError):
            PendingFriendRequest.objects.create(from_user=self.user, to_user=user2)

    def test_friendrequest_reverse_is_allowed(self):
        """Creating a friend request in the reverse direction is allowed"""
        PendingFriendRequest.objects.all().delete()
        user2 = User.objects.create(username="user2")
        PendingFriendRequest.objects.create(from_user=self.user, to_user=user2)

        # Reverse direction is allowed (handled in view)
        req = PendingFriendRequest.objects.create(from_user=user2, to_user=self.user)
        self.assertIsNotNone(req)

    def test_adding_friend_is_symmetrical(self):
        """Adding a friend adds the relationship in both directions"""
        user2 = User.objects.create(username="user2")
        self.user.friends.add(user2)

        self.assertIn(user2, self.user.friends.all())
        self.assertIn(self.user, user2.friends.all())

    def test_removing_friend_is_symmetrical(self):
        """Removing a friend removes the relationship in both directions"""
        user2 = User.objects.create(username="user2")
        self.user.friends.add(user2)

        self.user.friends.remove(user2)

        self.assertNotIn(user2, self.user.friends.all())
        self.assertNotIn(self.user, user2.friends.all())

    def test_register_with_invalid_studiengang_type_fails(self):
        """Register fails when studiengang is of invalid type"""
        data = {
            "username": "x",
            "password": "StrongPass123!",
            "studiengang": "abc"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("studiengang", serializer.errors)

    def test_login_serializer_missing_password_fails(self):
        """Login serializer fails when password is missing"""
        serializer = LoginSerializer(data={"username": "test"})
        self.assertFalse(serializer.is_valid())

    def test_streak_without_study_days_is_zero(self):
        """User streak is zero when there are no study days"""
        self.assertEqual(self.user.streak, 0)

    def test_creating_studyday_updates_streak(self):
        """Creating a study day updates the user's streak"""
        StudyDay.objects.create(user=self.user, date=date.today())
        self.user.refresh_from_db()
        self.assertEqual(self.user.streak, 1)

    def test_get_user_rank_unknown_user(self):
        """Getting rank for unknown user returns None"""
        fake_id = uuid.uuid4()
        users_qs = User.objects.filter(id=self.user.id)
        rank = get_user_rank(fake_id, users_qs)
        self.assertIsNone(rank)
                
    def test_same_rank_for_equal_points(self):
        """Users with the same points should have the same rank"""
        user1 = User.objects.create(username="user1", iq_score=100)
        user2 = User.objects.create(username="user2", iq_score=100)
        
        rank1 = get_user_rank(user1.id, User.objects.all())
        rank2 = get_user_rank(user2.id, User.objects.all())
        
        self.assertEqual(rank1, rank2)
     
    
    def test_different_points_different_ranks(self):
        """Users with different points should have different ranks"""
        user1 = User.objects.create(username="user1", iq_score=150)
        user2 = User.objects.create(username="user2", iq_score=100)

        rank1 = get_user_rank(user1.id, User.objects.all())
        rank2 = get_user_rank(user2.id, User.objects.all())
        

        self.assertNotEqual(rank1, rank2)

    def test_get_user_rank_highest_iq_score(self):
        """User with highest IQ gets rank 1"""
        test_users = []

        user2 = User.objects.create(username="user2", iq_score=100)
        test_users.append(user2)
        user3 = User.objects.create(username="user3", iq_score=200)
        test_users.append(user3)

        self.user.iq_score = 150
        self.user.save()
        test_users.append(self.user)

        # QuerySet nur für Test-Users
        users_qs = User.objects.filter(id__in=[u.id for u in test_users])

        # get ranks
        ranks = {u.username: get_user_rank(u.id, users_qs) for u in test_users}

        # sort by rank
        sorted_by_rank = [username for username, _ in sorted(ranks.items(), key=lambda x: x[1])]

        # expected order: highest IQ first
        expected_order = ["user3", "testuser", "user2"]

        self.assertEqual(sorted_by_rank, expected_order)
        