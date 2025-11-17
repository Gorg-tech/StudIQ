from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout, get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from .models import StudyDay
from datetime import timedelta, date

class RegisterView(APIView):
    permission_classes = []  # Allow unauthenticated access
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # Log the user in (creates session)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        # Explicitly return serializer errors so missing studiengang is visible to client
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []  # Allow unauthenticated access

    def post(self, request):
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
    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."})

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})


class UserStatsView(APIView):
    """Return current user's stats (used by frontend at /api/users/me/stats/)."""
    permission_classes = [IsAuthenticated]

    def get_user_rank(self, user_id):
        """Berechnet die Position eines Users im Leaderboard."""
        User = get_user_model()
        try:
            target = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        # Anzahl der Nutzer mit höherer streak + 1
        higher = User.objects.filter(streak__gt=target.streak).values('streak').distinct().count()
        return higher + 1

    def get(self, request):
        serializer = UserSerializer(request.user)
        data = serializer.data
        data['rank'] = self.get_user_rank(request.user.id)
        data['streak'] = calculate_streak(request.user)
        return Response(data)

def calculate_streak(user):
    days = StudyDay.objects.filter(user=user).values_list('date', flat=True).order_by('-date')
    streak = 0
    last_day = date.today()

    for d in days:
        if last_day - d in [timedelta(days=0), timedelta(days=1)]:
            streak += 1
            last_day = d
        else:
            break
    return streak

def calculate_longest_streak(user):
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
# def register_study_activity(user):
#    today = date.today()
#    StudyDay.objects.get_or_create(user=user, date=today)

class StudyCalendarView(APIView):
    permission_classes = [IsAuthenticated]
    # get all study days and streak for the current user
    def get(self, request):
        user = request.user
        days = StudyDay.objects.filter(user=user)
        data = {
            "streak": calculate_streak(user),
            "longest_streak": calculate_longest_streak(user),
            "days": [d.date.isoformat() for d in days]
        }
        return Response(data)