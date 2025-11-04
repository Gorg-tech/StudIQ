from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout, get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

class RegisterView(APIView):
    permission_classes = []  # Allow unauthenticated access
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # Log the user in (creates session)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
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
        return Response(data)