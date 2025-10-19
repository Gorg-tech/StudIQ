from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.db.models import Q
from .models import (
    Quiz,
    Question,
    Lernset,
    QuizProgress,
    Achievement,
    QuizSession,
    Feedback,
    Studiengang,
    Modul,
)
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    LernsetSerializer,
    QuizProgressSerializer,
    AchievementSerializer,
    QuizSessionSerializer,
    FeedbackSerializer,
    StudiengangSerializer,
    ModulSerializer,
    ModulDetailSerializer, 
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Not found."}, status=404)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class LernsetViewSet(viewsets.ModelViewSet):
    queryset = Lernset.objects.all()
    serializer_class = LernsetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
      # Automatically set the created_by to the current user
      serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Not found."}, status=404)

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

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Not found."}, status=404)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ModulDetailSerializer(instance)  # Use ModulDetailSerializer here instead of ModulSerializer
        return Response(serializer.data)


class QuizzesByLernsetView(ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lernset_id = self.kwargs["lernset_id"]
        return Quiz.objects.filter(lernset_id=lernset_id)


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "")
        filter_type = request.query_params.get("filter", None)

        results = {
            "lernsets": [],
            "quizzes": [],
            "modules": [],
            "studiengaenge": [],
        }

        # If no query, just return first 10 of the filtered type (or all types if no filter)
        if not query:
            if filter_type:
                if filter_type.lower() == "lernsets":
                    lernsets = Lernset.objects.all()[:10]
                    results["lernsets"] = LernsetSerializer(lernsets, many=True).data
                elif filter_type.lower() == "quizzes":
                    quizzes = Quiz.objects.all()[:10]
                    results["quizzes"] = QuizSerializer(quizzes, many=True).data
                elif filter_type.lower() == "modules":
                    modules = Modul.objects.all()[:10]
                    results["modules"] = ModulSerializer(modules, many=True).data
                elif filter_type.lower() == "studiengaenge":
                    studiengaenge = Studiengang.objects.all()[:10]
                    results["studiengaenge"] = StudiengangSerializer(
                        studiengaenge, many=True
                    ).data
            else:
                # No filter, return first 2 of each type
                lernsets = Lernset.objects.all()[:2]
                results["lernsets"] = LernsetSerializer(lernsets, many=True).data
                quizzes = Quiz.objects.all()[:2]
                results["quizzes"] = QuizSerializer(quizzes, many=True).data
                modules = Modul.objects.all()[:2]
                results["modules"] = ModulSerializer(modules, many=True).data
                studiengaenge = Studiengang.objects.all()[:2]
                results["studiengaenge"] = StudiengangSerializer(
                    studiengaenge, many=True
                ).data
            return Response(results)

        # Apply filter if specified
        if filter_type:
            if filter_type.lower() == "lernsets":
                # Search only lernsets
                lernsets = Lernset.objects.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )
                results["lernsets"] = LernsetSerializer(lernsets, many=True).data

            elif filter_type.lower() == "quizzes":
                # Search only quizzes
                quizzes = Quiz.objects.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )
                results["quizzes"] = QuizSerializer(quizzes, many=True).data

            elif filter_type.lower() == "modules":
                # Search only modules
                modules = Modul.objects.filter(
                    Q(name__icontains=query)
                    | Q(description__icontains=query)
                    | Q(modulId__icontains=query)
                )
                results["modules"] = ModulSerializer(modules, many=True).data

            elif filter_type.lower() == "studiengaenge":
                # Search only study programs
                studiengaenge = Studiengang.objects.filter(
                    Q(name__icontains=query)
                    | Q(description__icontains=query)
                    | Q(id__icontains=query)
                )
                results["studiengaenge"] = StudiengangSerializer(
                    studiengaenge, many=True
                ).data
        else:
            # Search across all models
            lernsets = Lernset.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            results["lernsets"] = LernsetSerializer(lernsets, many=True).data

            quizzes = Quiz.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            results["quizzes"] = QuizSerializer(quizzes, many=True).data

            modules = Modul.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(modulId__icontains=query)
            )
            results["modules"] = ModulSerializer(modules, many=True).data

            # Added search for study programs
            studiengaenge = Studiengang.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(id__icontains=query)
            )
            results["studiengaenge"] = StudiengangSerializer(
                studiengaenge, many=True
            ).data

        return Response(results)
