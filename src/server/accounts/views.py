
"""
Account-related API views for user registration, authentication, profile, stats, and study streaks.

This file provides endpoints for user registration, login, logout, profile retrieval, user stats,
CSRF cookie handling, and study streak/calendar logic. It also includes utility functions for
calculating user rank and streaks.
"""

from datetime import timedelta, date
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .models import StudyDay, PendingFriendRequest, Friendship

class RegisterView(APIView):
    """
    API endpoint for user registration.
    Allows unauthenticated users to create a new account and logs them in upon success.
    """
    permission_classes = []  # Allow unauthenticated access

    def post(self, request):
        """
        Register a new user and log them in.

        Args:
            request (Request): The HTTP request containing registration data.

        Returns:
            Response: User data on success, or validation errors on failure.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # Log the user in (creates session)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        # Explicitly return serializer errors so missing studiengang is visible to client
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    API endpoint for user login.
    Authenticates user credentials and creates a session on success.
    """
    permission_classes = []  # Allow unauthenticated access

    def post(self, request):
        """
        Authenticate and log in a user.

        Args:
            request (Request): The HTTP request containing login credentials.

        Returns:
            Response: User data on success, or error message on failure.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response(UserSerializer(user).data)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """
    API endpoint for user logout.
    Logs out the current user and ends their session.
    """
    def post(self, request):
        """
        Log out the current user.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: Success message.
        """
        logout(request)
        return Response({"detail": "Successfully logged out."})

class MeView(APIView):
    """
    API endpoint to retrieve the current authenticated user's profile data.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the current user's profile data.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: Serialized user data.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@ensure_csrf_cookie
def csrf(request):
    """
    Set the CSRF cookie for the client.

    Args:
        request (Request): The HTTP request.

    Returns:
        JsonResponse: Confirmation that the CSRF cookie is set.
    """
    return JsonResponse({'detail': 'CSRF cookie set'})


def get_user_rank(user_id, user_set):
    """
    Calculate the leaderboard rank of a user based on their iq_score.

    Args:
        user_id (int): The ID of the user.
        user_set (QuerySet): The user model queryset to search in.
    Returns:
        int or None: The user's rank (1-based), or None if user does not exist.
    """
    try:
        target = user_set.get(id=user_id)
    except user_set.DoesNotExist:
        return None
    # Number of users with a higher iq_score + 1
    higher = user_set.filter(iq_score__gt=target.iq_score).values('iq_score')\
                            .distinct().count()
    return higher + 1

class UserStatsView(APIView):
    """
    API endpoint to return the current user's statistics, including leaderboard rank.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the current user's statistics and leaderboard rank.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: User stats and rank.
        """
        serializer = UserSerializer(request.user)
        data = serializer.data
        data['rank'] = get_user_rank(request.user.id, get_user_model().objects.all())
        return Response(data)

def calculate_streak(user):
    """
    Calculate the current study streak for a user and update the user's streak field.

    Args:
        user (User): The user instance.

    Returns:
        int: The current streak count.
    """
    days = StudyDay.objects.filter(user=user).values_list('date', flat=True).order_by('-date')
    streak = 0
    last_day = date.today()

    for d in days:
        if last_day - d in [timedelta(days=0), timedelta(days=1)]:
            streak += 1
            last_day = d
        else:
            break

    user.streak = streak
    user.save(update_fields=['streak'])
    return streak

def calculate_longest_streak(user):
    """
    Calculate the longest consecutive study streak for a user.

    Args:
        user (User): The user instance.

    Returns:
        int: The longest streak count.
    """
    days = StudyDay.objects.filter(user=user).values_list('date', flat=True).order_by('date')

    if not days:
        return 0

    longest_streak = 0
    current_streak = 1

    for i in range(1, len(days)):
        if days[i] - days[i - 1] == timedelta(days=1):
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
    longest_streak = max(longest_streak, current_streak)
    return longest_streak

# Upon quiz completion, update streak by calling the following:
def register_study_activity(user):
    """
    Register today's study activity for the user and update their streak.

    Args:
        user (User): The user instance.
    """
    today = date.today()
    StudyDay.objects.get_or_create(user=user, date=today)
    calculate_streak(user)

class StudyCalendarView(APIView):
    """
    API endpoint to retrieve the user's study calendar and streak information.
    Returns all study days, current streak, and longest streak for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all study days and streak information for the current user.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: Dictionary with streak, longest streak, and list of study days.
        """
        user = request.user
        days = StudyDay.objects.filter(user=user)
        data = {
            "streak": calculate_streak(user),
            "longest_streak": calculate_longest_streak(user),
            "days": [d.date.isoformat() for d in days]
        }
        return Response(data)

class FriendRequestsView(APIView):
    """
    API endpoint to retrieve the user's pending friend requests.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all pending friend requests for the current user.

        Args:
            request (Request): The HTTP request.
        Returns:
            Response: List of pending friend requests.
        """
        user = request.user
        requests = PendingFriendRequest.objects.filter(to_user=user)
        data = [{
            "from_user": req.from_user.username,
            "sent_at": req.sent_at.isoformat()
        } for req in requests]
        return Response(data)

    def post(self, request):
        """
        Send a friend request to another user or accept a friend request if they sent it first.

        Args:
            request (Request): The HTTP request containing 'to_user' username.

        Returns:
            Response: Success message or error.
        """
        from_user = request.user
        to_username = request.data.get('to_user')
        try:
            to_user = get_user_model().objects.get(username=to_username)
            if PendingFriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
                return Response({'error': 'Friend request already sent.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if PendingFriendRequest.objects.filter(from_user=to_user, to_user=from_user).exists():
                # Accept the friend request
                Friendship.objects.create(user=from_user, friend=to_user)
                Friendship.objects.create(user=to_user, friend=from_user)
                PendingFriendRequest.objects.filter(from_user=to_user, to_user=from_user).delete()
                return Response({'detail': 'Friend request accepted.'}, status=status.HTTP_200_OK)
            if Friendship.objects.filter(user=from_user, friend=to_user).exists():
                return Response({'error': 'You are already friends.'},
                                status=status.HTTP_400_BAD_REQUEST)
            PendingFriendRequest.objects.create(from_user=from_user, to_user=to_user)
            return Response({'detail': 'Friend request sent.'}, status=status.HTTP_201_CREATED)
        except get_user_model().DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        """
        Decline a friend request from another user.

        Args:
            request (Request): The HTTP request containing 'from_user' username.
        Returns:
            Response: Success message or error.
        """
        to_user = request.user
        from_username = request.data.get('from_user')
        try:
            from_user = get_user_model().objects.get(username=from_username)
            req = PendingFriendRequest.objects.filter(from_user=from_user, to_user=to_user)
            if req.exists():
                req.delete()
                return Response({'detail': 'Friend request declined.'}, status=status.HTTP_200_OK)
            return Response({'error': 'No such friend request.'}, status=status.HTTP_404_NOT_FOUND)
        except get_user_model().DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class FriendsListView(APIView):
    """
    API endpoint to retrieve the user's friends list.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all friends for the current user.

        Args:
            request (Request): The HTTP request.
        Returns:
            Response: List of friends.
        """
        user = request.user
        friends = user.friendships.all()
        data = [{
            "friend_username": f.friend.username,
            "since": f.created_at.isoformat()
        } for f in friends]
        return Response(data)
