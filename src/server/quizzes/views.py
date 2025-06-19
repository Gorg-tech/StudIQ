from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, Question, Lernset
from .serializers import QuizSerializer, QuestionSerializer, LernsetSerializer

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
