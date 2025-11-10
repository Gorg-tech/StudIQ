from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    AnswerOption
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
    AnswerOptionSerializer,
    QuizForLernsetSerializer
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from itertools import chain
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserSerializer

class AnswerOptionViewSet(viewsets.ModelViewSet):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # schnelle Debug-Ausgaben (entfernen/ersetzen durch logger in Prod)
        print("AnswerOption.create headers:", dict(request.headers))
        print("AnswerOption.create content_type:", request.content_type)
        print("AnswerOption.create body:", request.data)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # zeigen, welche Validierungsfehler vorliegen
            print("AnswerOption.create validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Not found."}, status=404)
    
    def perform_create(self, serializer):
        # Automatically set the created_by to the current user
        serializer.save(created_by=self.request.user)

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
    permission_classes = [AllowAny]


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


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet für das Leaderboard. Unterstützt zwei query-Parameter:
    - limit: Anzahl der Top-Nutzer, die vorne angezeigt werden (z.B. 3)
    - around: Anzahl der Nutzer vor/nach dem aktuellen User, die angezeigt werden

    Gibt zurück: {
      users: [ ...serialized users in display order... ],
      current_user_rank: int,
      top_count: int,
      around: int
    }
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_user_rank(self, user_id):
        """Berechnet die Position eines Users im Leaderboard."""
        User = get_user_model()
        try:
            target = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        # Anzahl der höheren streaks + 1
        higher = User.objects.filter(streak__gt=target.streak).values('streak').distinct().count()
        return higher + 1

    def get_users_around(self, user_id, before=1, after=1): 
        """Holt Nutzer vor und nach dem gegebenen User. Returns a list: [user_before_n, ..., user_before_1, current_user, user_after_1, ...] """ 
        User = get_user_model()
        try: 
            current_user = User.objects.get(id=user_id) 
        except User.DoesNotExist: 
            return [] 
        
        # Robust approach: build ordered list of user ids by rank and slice by index.
        ordered_ids = list(User.objects.order_by('-streak', 'id').values_list('id', flat=True)) 
        try: 
            idx = ordered_ids.index(current_user.id) 
        except ValueError: 
            return [current_user] 
        start = max(0, idx - before) 
        end = min(len(ordered_ids), idx + after + 1) 
        slice_ids = ordered_ids[start:end] 
        # Fetch the user objects for these ids and preserve the order from slice_ids 
        users_qs = User.objects.filter(id__in=slice_ids) 
        users_map = {u.id: u for u in users_qs} 
        ordered_users = [users_map[_id] for _id in slice_ids if _id in users_map] 
        return ordered_users

    def list(self, request, *args, **kwargs):
        # Parse parameters
        try:
            top_count = max(0, int(request.query_params.get('limit', 3)))
        except (ValueError, TypeError):
            top_count = 3

        try:
            around = max(0, int(request.query_params.get('around', 1)))
        except (ValueError, TypeError):
            around = 1

        User = get_user_model()

        # Fetch top users
        top_users = list(User.objects.order_by('-streak', 'id')[:top_count]) if top_count > 0 else []

        # Fetch users around current user
        around_users = []
        if request.user and request.user.is_authenticated and around > 0:
            around_users = self.get_users_around(request.user.id, before=around, after=around)
            
            # check if last user in around_users is last of everyone and if yes, set has_more_after to False
            last_around_user = around_users[-1] if around_users else None
            first_around_user = around_users[0] if around_users else None
            all_users = list(User.objects.order_by('-streak', 'id'))

            idx_top_last = all_users.index(top_users[-1]) if top_users else -1
            idx_around_first = all_users.index(first_around_user) if first_around_user else -1

            has_more_before = idx_around_first > idx_top_last + 1
            has_more_after = User.objects.order_by('-streak', 'id').last().id != last_around_user.id if last_around_user else True

        # Combine top and around, preserving order and removing duplicates
        combined = list(top_users)
        for u in around_users:
            if u not in combined:
                combined.append(u)

        # Serialize
        serialized = self.get_serializer(combined, many=True).data

        for item in serialized:
            item['rank'] = self.get_user_rank(item['id'])

        return Response({
            'users': serialized,
            'top_count': top_count,
            'around': around,
            'has_more_after': has_more_after,
            'has_more_before': has_more_before
        })

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        filter_type = request.query_params.get("filter", None)

        # allow client to request more results (default 15, max 100)
        limit_param = request.query_params.get("limit")
        try:
            limit = max(1, min(int(limit_param), 100)) if limit_param is not None else 15
        except (ValueError, TypeError):
            limit = 15

        results = {
            "lernsets": [],
            "quizzes": [],
            "modules": [],
            "studiengaenge": [],
        }

        # If no query, just return first N of the filtered type (or small sample of all types)
        if not query:
            if filter_type:
                if filter_type.lower() == "lernsets":
                    lernsets = Lernset.objects.all()[:limit]
                    results["lernsets"] = LernsetSerializer(lernsets, many=True).data
                elif filter_type.lower() == "quizzes":
                    quizzes = Quiz.objects.all()[:limit]
                    results["quizzes"] = QuizSerializer(quizzes, many=True).data
                elif filter_type.lower() == "modules":
                    modules = Modul.objects.all()[:limit]
                    results["modules"] = ModulSerializer(modules, many=True).data
                elif filter_type.lower() == "studiengaenge":
                    studiengaenge = Studiengang.objects.all()[:limit]
                    results["studiengaenge"] = StudiengangSerializer(
                        studiengaenge, many=True
                    ).data
            else:
                # No filter, return a small sample of each type
                sample = min(2, limit)
                lernsets = Lernset.objects.all()[:sample]
                results["lernsets"] = LernsetSerializer(lernsets, many=True).data
                quizzes = Quiz.objects.all()[:sample]
                results["quizzes"] = QuizSerializer(quizzes, many=True).data
                modules = Modul.objects.all()[:sample]
                results["modules"] = ModulSerializer(modules, many=True).data
                studiengaenge = Studiengang.objects.all()[:sample]
                results["studiengaenge"] = StudiengangSerializer(
                    studiengaenge, many=True
                ).data
            return Response(results)

        # Apply filter if specified
        lernsets_qs = Lernset.objects.none()
        quizzes_qs = Quiz.objects.none()
        modules_qs = Modul.objects.none()
        studiengaenge_qs = Studiengang.objects.none()

        if not filter_type or filter_type.lower() == "lernsets":
            lernsets_qs = Lernset.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )[:limit]

        if not filter_type or filter_type.lower() == "quizzes":
            quizzes_qs = Quiz.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )[:limit]

        if not filter_type or filter_type.lower() == "modules":
            modules_qs = Modul.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(modulId__icontains=query)
            )[:limit]

        if not filter_type or filter_type.lower() == "studiengaenge":
            studiengaenge_qs = Studiengang.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(id__icontains=query)
            )[:limit]

        # Combine all results and limit to top 'limit' across types
        all_items = list(chain(lernsets_qs, quizzes_qs, modules_qs, studiengaenge_qs))[:limit]

        # Serialize and categorize
        for item in all_items:
            if isinstance(item, Lernset):
                results["lernsets"].append(LernsetSerializer(item).data)
            elif isinstance(item, Quiz):
                results["quizzes"].append(QuizSerializer(item).data)
            elif isinstance(item, Modul):
                results["modules"].append(ModulSerializer(item).data)
            elif isinstance(item, Studiengang):
                results["studiengaenge"].append(StudiengangSerializer(item).data)

        return Response(results)

class SuggestedQuizzesView(ListAPIView):
    serializer_class = QuizForLernsetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.studiengang:
            return Quiz.objects.none()
        
        # Get all modules for the user's studiengang
        modules = user.studiengang.module.all()
        
        # Get all lernsets for these modules
        lernsets = Lernset.objects.filter(modul__in=modules)
        
        # Get quizzes from these lernsets, ordered by creation date, limit to 3
        quizzes = Quiz.objects.filter(lernset__in=lernsets).order_by('-created_at')[:3]
        
        return quizzes