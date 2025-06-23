from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Quiz, Question, Lernset, QuizProgress, Achievement, QuizSession, Feedback, Studiengang, Modul
from .serializers import QuizSerializer, QuestionSerializer, LernsetSerializer, QuizProgressSerializer, AchievementSerializer, QuizSessionSerializer, FeedbackSerializer, StudiengangSerializer, ModulSerializer
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    
class LernsetViewSet(viewsets.ModelViewSet):
    queryset = Lernset.objects.all()
    serializer_class = LernsetSerializer
    permission_classes = [IsAuthenticated]

class QuizProgressViewSet(viewsets.ModelViewSet):
    serializer_class = QuizProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return QuizProgress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
class QuizSessionViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return QuizSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StudiengangViewSet(viewsets.ModelViewSet):
    queryset = Studiengang.objects.all()
    serializer_class = StudiengangSerializer
    permission_classes = [IsAuthenticated]

class ModulViewSet(viewsets.ModelViewSet):
    queryset = Modul.objects.all()
    serializer_class = ModulSerializer
    permission_classes = [IsAuthenticated]

class LernsetsByModuleView(ListAPIView):
    serializer_class = LernsetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        module_id = self.kwargs['module_id']
        return Lernset.objects.filter(modul_id=module_id)

class QuizzesByLernsetView(ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lernset_id = self.kwargs['lernset_id']
        return Quiz.objects.filter(lernset_id=lernset_id)

class QuestionsByQuizView(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        return Question.objects.filter(quiz_id=quiz_id)

# functionality for login session handling
 # ---- liefert CSRF-Cookie aus (1. Schritt im FE) ----
@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    token = get_token(request)               # erzeugt/holt Token
    resp = HttpResponse(status=204)
    resp.set_cookie(
        "csrftoken",
        token,
        samesite="Lax",        # Dev-Einstellung; Prod → 'None' + Secure
        secure=False,          # Prod: True (HTTPS)
        httponly=False,
    )
    return resp

# ---- Session-Login (2. Schritt im FE) --------------
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    user = authenticate(
        request,
        username=request.data.get("username"),
        password=request.data.get("password"),
    )
    if user:
        login(request, user)            # setzt sessionid-Cookie
        return Response({"detail": "ok"})
    return Response(
        {"detail": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
    )
