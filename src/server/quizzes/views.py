"""
View classes for quiz-related API endpoints.

This file contains all Django REST Framework viewsets and API views for the quiz app.
It provides endpoints for CRUD operations on quizzes, questions, answer options, lernsets, modules,
achievements, quiz progress, sessions, feedback, leaderboard, search, and quiz completion logic.
"""

import re
from itertools import chain
from math import exp, floor
from pymysql import IntegrityError
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, F
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.views import get_user_rank
from accounts.serializers import LeaderboardUserSerializer
from accounts.views import register_study_activity
from .models import (
    Quiz,
    Question,
    Lernset,
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
    FeedbackSerializer,
    StudiengangSerializer,
    ModulSerializer,
    ModulDetailSerializer,
    AnswerOptionSerializer,
    QuizForLernsetSerializer
)

class AnswerOptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing AnswerOption objects.
    Supports CRUD operations for answer options of quiz questions.
    """
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class QuizViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Quiz objects.
    Handles creation, update, and deletion of quizzes,
    with permission checks for creators and moderators.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_url_kwarg = 'quiz_id'
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Not found."}, status=404)


    def perform_create(self, serializer):
        # Automatically set the created_by to the current user
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.created_by and request.user.role != 'MODERATOR':
            return Response({"detail": "You do not have permission to edit this quiz."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.created_by and request.user.role != 'MODERATOR':
            return Response({"detail": "You do not have permission to delete this quiz."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def start(self, request, quiz_id=None):
        """
        Creates a new QuizSession for the user and quiz.

        Returns (in response):
        dict: {
            "session_id": uuid,
            "title": str,
            "description": str,
            "first_question": {
                "id": uuid,
                "text": str,
                "type": str,
                "answer_options": [
                    {
                        "id": uuid,
                        "text": str
                    }, ...
                ]
            },
            "total_questions": int
        }
        """
        user = request.user
        quiz = self.get_object()
        quiz_session = QuizSession.objects.filter(user=user, quiz=quiz, end_time__isnull=True).first()

        # If an active session already exists, reset it, else create a new one
        if quiz_session is not None:
            quiz_session.start_time = timezone.now()
            quiz_session.total_answers = 0
            quiz_session.correct_answers = 0
            quiz_session.save()
        else:
            try:
                quiz_session = QuizSession.objects.create(
                    user=user,
                    quiz=quiz,
                    start_time=timezone.now()
                )
            except IntegrityError:
                return Response({"detail": "An active quiz session already exists."},
                                status=status.HTTP_409_CONFLICT)
        
        # Get first question
        questions = list(quiz.questions.all().order_by('id'))
        if not questions:
            return Response({"detail": "No questions in quiz."}, status=400)
        
        first_question = questions[0]
        return Response({
        "session_id": str(quiz_session.id),
        "title": quiz.title,
        "description": quiz.description,
        "first_question": {
            "id": str(first_question.id),
            "text": first_question.text,
            "type": first_question.type,
            "answer_options": [{"id": str(o.id), "text": o.text} for o in first_question.answer_options.all()]
        },
        "total_questions": len(questions)
    }, status=201)

    @action(detail=True, methods=['post'])
    def answer(self, request, quiz_id=None):
        """
        Submits an answer for the current question in the active QuizSession.

        Expects (in request data):
        dict: {
            "question_id": uuid,
            "selected_option_ids": [uuid, ...]
        }

        Returns (in response):
        dict: {
            "is_correct": bool,
            "correct_answers": [uuid, ...],
            "total_questions": int,
            "next_question": {
                "id": uuid,
                "text": str,
                "type": str,
                "answer_options": [
                    {
                        "id": uuid,
                        "text": str
                    }, ...
                ]
            }
        }
        """
        user = request.user
        quiz = self.get_object()
        quiz_session = QuizSession.objects.filter(user=user, quiz=quiz,
                                                  end_time__isnull=True).first()
        if not quiz_session:
            return Response({"detail": "No active quiz session found."},
                            status=status.HTTP_404_NOT_FOUND)

        question_id = request.data.get("question_id")
        selected_option_ids = request.data.get("selected_option_ids", [])

        # Get all questions for the quiz
        questions = list(quiz.questions.all().order_by('id'))
        current_question_index = quiz_session.total_answers

        # Validate question
        if current_question_index >= len(questions):
            return Response({"detail": "No more questions available."},
                            status=status.HTTP_404_NOT_FOUND)
        question = questions[current_question_index]
        if str(question.id) != str(question_id):
            return Response({"detail": "Question ID does not match the current question."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate selected options
        valid_option_ids = set(
            str(option.id) for option in question.answer_options.all()
        )
        if not all(option_id in valid_option_ids for option_id in selected_option_ids):
            return Response({"detail": "Invalid answer option IDs."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check correctness
        correct_option_ids = set(
            str(option.id) for option in question.answer_options.filter(is_correct=True)
        )
        is_correct = set(selected_option_ids) == correct_option_ids

        # Update quiz session stats
        quiz_session.total_answers += 1
        if is_correct:
            quiz_session.correct_answers += 1
        quiz_session.save()

        # Build response
        response_data = {
            "is_correct": is_correct,
            "correct_answers": list(correct_option_ids),
            "total_questions": len(questions)
        }

        # Determine next question
        if current_question_index != len(questions) - 1:
            next_question = questions[current_question_index + 1]
            response_data["next_question"] = {
                "id": str(next_question.id),
                "text": next_question.text,
                "type": next_question.type,
                "answer_options": [
                    {
                        "id": str(option.id),
                        "text": option.text
                    } for option in next_question.answer_options.all()
                ]
            }
        else:
            response_data["next_question"] = None

        return Response(response_data)

    @action(detail=True, methods=['get'])
    def sessions(self, request, quiz_id=None):
        """
        Retrieves the user's completed QuizSessions for the specified quiz.

        Returns (in response):
        list: [
            dict: {
                "start_time": datetime,
                "end_time": datetime or null,
                "correct_answers": int,
                "total_answers": int
            }, ...
        ]
        """
        user = request.user
        quiz = self.get_object()

        quiz_sessions = QuizSession.objects.filter(user=user, quiz=quiz, end_time__isnull=False).order_by('start_time')

        dict_list = []
        for quiz_session in quiz_sessions:
            dict_list.append({
                "start_time": quiz_session.start_time,
                "end_time": quiz_session.end_time,
                "correct_answers": quiz_session.correct_answers,
                "total_answers": quiz_session.total_answers
            })

        return Response(dict_list)

    @action(detail=True, methods=['post'])
    def complete(self, request, quiz_id=None):
        """
        Calculates the points the user receives, updates the user and returns results.

        Returns (in response):
        dict: {
            "base_points": int,
            "perfect_bonus_points": int,
            "streak_bonus_points": int,
            "prev_iq": int,
            "total_answers": int,
            "correct_answers": int
        }
        """
        user = request.user
        quiz = self.get_object()
        quiz_sessions = QuizSession.objects.filter(user=user, quiz=quiz)
        attempts = quiz_sessions.count()
        quiz_session = quiz_sessions.filter(end_time__isnull=True).first()
        if not quiz_session:
            return Response({"detail": "No active quiz session found."},
                            status=status.HTTP_404_NOT_FOUND)
        register_study_activity(user)
        streak = user.streak
        accuracy = quiz_session.correct_answers / quiz_session.total_answers\
            if quiz_session.total_answers > 0 else 0
        had_perfect_before = False

        # calculate if this is the first perfect
        had_perfect_before = quiz_sessions.filter(end_time__isnull=False)\
        .filter(correct_answers=F('total_answers')).exclude(total_answers=0).exists()

        # formulas
        # score becomes less with more attempts
        attempt_multiplier = exp((-0.5 if had_perfect_before else -0.2) * (attempts - 1))
        # based on accuracy and the amount of questions answered
        base_points = quiz_session.total_answers ** (accuracy) * (0.2 if had_perfect_before else 1)
        # adds 50% of the base points when reaching perfect score
        perfect_bonus = 0.5 if not had_perfect_before and accuracy == 1.0 else 0
        # adds up to 25% of the base points with a higher streak
        streak_bonus = 0.25 * (1 - exp(-0.33 * streak)) if not had_perfect_before else 0

        base_points = floor(base_points * attempt_multiplier)
        perfect_bonus_points = floor(base_points * perfect_bonus)
        streak_bonus_points = floor(base_points * streak_bonus)

        # update user and quiz progress
        prev_iq = user.iq_score
        user.iq_score = prev_iq + floor(base_points + perfect_bonus_points + streak_bonus_points)
        user.solved_quizzes += 1
        user.save()

        quiz_session.end_time = timezone.now()
        quiz_session.save()

        return Response({
            "attempts": attempts,
            "streak": streak,
            "base_points": base_points,
            "perfect_bonus_points": perfect_bonus_points,
            "streak_bonus_points": streak_bonus_points,
            "prev_iq": prev_iq,
            "total_answers": quiz_session.total_answers,
            "correct_answers": quiz_session.correct_answers
        })

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Question objects.
    Supports CRUD operations for quiz questions.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class LernsetViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Lernset objects.
    Handles creation, update, and deletion of lernsets, with permission checks
    for creators and moderators.
    """
    queryset = Lernset.objects.all()
    serializer_class = LernsetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the created_by to the current user
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Not found."}, status=404)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.created_by and request.user.role != 'MODERATOR':
            return Response({"detail": "You do not have permission to edit this lernset."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.created_by and request.user.role != 'MODERATOR':
            return Response({"detail": "You do not have permission to delete this lernset."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Feedback objects.
    Allows users to submit and view feedback for quizzes.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudiengangViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Studiengang (field of study) objects.
    Allows listing, creating, updating, and deleting study programs.
    """
    queryset = Studiengang.objects.all()
    serializer_class = StudiengangSerializer
    permission_classes = [AllowAny]


class ModulViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Modul (module) objects.
    Allows listing, creating, updating, and deleting modules.
    Uses a detailed serializer for retrieve actions.
    """
    queryset = Modul.objects.all()
    serializer_class = ModulSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Not found."}, status=404)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Use ModulDetailSerializer here instead of ModulSerializer
        serializer = ModulDetailSerializer(instance)
        # Use ModulDetailSerializer here instead of ModulSerializer
        serializer = ModulDetailSerializer(instance)
        return Response(serializer.data)


class QuizzesByLernsetView(ListAPIView):
    """
    API endpoint for listing all quizzes belonging to a specific Lernset.
    """
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lernset_id = self.kwargs["lernset_id"]
        return Quiz.objects.filter(lernset_id=lernset_id)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for the leaderboard.
    Returns top users and users around the current user, with rank, streak and IQ information.
    Supports query parameters for how many top users to show (limit)
    and how many users to show around the current user (around)
    and in what category ('all', 'friends', 'studiengang').
    """
    serializer_class = LeaderboardUserSerializer
    permission_classes = [IsAuthenticated]

    def get_users_around(self, user_id, user_model, before=1, after=1):
        """
        Retrieves users in front and behind the user.
        Args:
            user_id (long): The id of the current user
            user_model (QuerySet): The user model queryset to search in
            before (int): how many users to return in front
            after (int): how many users to return behind
        Returns:
            list: [user_before_n, ..., user_before_1, current_user, user_after_1, ..., user_after_m]
        """
        current_user = user_model.get(id=user_id)

        # reduce model to ordered ids only for indexing
        ordered_ids = list(user_model.values_list('id', flat=True))
        try:
            idx = ordered_ids.index(current_user.id)
        except ValueError:
            return [current_user]
        start = max(0, idx - before)
        end = min(len(ordered_ids), idx + after + 1)
        slice_ids = ordered_ids[start:end]
        # Fetch the user objects for these ids and preserve the order from slice_ids
        users_qs = user_model.filter(id__in=slice_ids)
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

        try:
            category = request.query_params.get('category', 'all').lower()
        except (ValueError, TypeError):
            category = 'all'

        user_model = get_user_model().objects.all()

        # Get subset of users based on category
        if category == 'friends':
            friends_ids = request.user.friends.values_list('id', flat=True)
            user_model = user_model.filter(Q(id__in=friends_ids) | Q(id=request.user.id))
        elif category == 'studiengang' and request.user.studiengang:
            user_model = user_model.filter(studiengang=request.user.studiengang)

        # Sort user_model by iq_score, fetch the first users and the users around current user
        # Note: Cannot use .only() with '_streak' since we need the @property to calculate it
        user_model = user_model.order_by('-iq_score', 'id')
        top_users = list(user_model[:top_count])
        around_users = self.get_users_around(request.user.id, user_model,
                                            before=around, after=around)

        # check if last user in around_users is last of everyone
        all_users = list(user_model)

        idx_top_last = all_users.index(top_users[-1]) if top_users else -1
        idx_around_first = all_users.index(around_users[0]) if around_users else -1

        has_more_before = idx_around_first > idx_top_last + 1
        has_more_after = user_model.last().id != around_users[-1].id if around_users else True

        # Combine top and around, preserving order and removing duplicates
        combined = list(top_users)
        for u in around_users:
            if u not in combined:
                combined.append(u)

        # Serialize
        serialized = self.get_serializer(combined, many=True).data

        for item in serialized:
            item['rank'] = get_user_rank(item['id'], user_model)

        return Response({
            'users': serialized,
            'top_count': top_count,
            'around': around,
            'has_more_after': has_more_after,
            'has_more_before': has_more_before
        })

class SearchView(APIView):
    """
    API endpoint for searching lernsets, quizzes, modules, and study programs.
    Supports filtering and relevance-based result ordering.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Gets all lernsets, quizzes, modules and studiengaenge
        that match the filter word given in the query param "q".
        The returned types can be limited by the "filter" query param,
        the amount of returned objects can be limited by the "limit" query param.

        Args:
            request (Request): The API GET Request including query params
        
        Returns:
            dict: {
                "lernsets": [...],
                "quizzes": [...],
                "modules": [...],
                "studiengaenge": [...]
            }
        """
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

        # Helper function to build Q object for multi-word search
        def build_search_q(fields, query):
            words = query.split()
            if not words:
                return Q()
            q_objects = Q()
            for word in words:
                word_q = Q()
                for field in fields:
                    word_q |= Q(**{f"{field}__icontains": word})
                q_objects &= word_q
            return q_objects

        # Increase limit for candidates to allow better sorting
        candidate_limit = min(limit * 4, 100)  # Collect more candidates for sorting

        if not filter_type or filter_type.lower() == "lernsets":
            lernsets_qs = Lernset.objects.filter(
                build_search_q(['title', 'description'], query)
            )[:candidate_limit]

        if not filter_type or filter_type.lower() == "quizzes":
            quizzes_qs = Quiz.objects.filter(
                build_search_q(['title', 'description'], query)
            )[:candidate_limit]

        if not filter_type or filter_type.lower() == "modules":
            modules_qs = Modul.objects.filter(
                build_search_q(['name', 'dozent_name', 'modulId'], query)
            )[:candidate_limit]

        if not filter_type or filter_type.lower() == "studiengaenge":
            studiengaenge_qs = Studiengang.objects.filter(
                build_search_q(['name', 'description', 'id'], query)
            )[:candidate_limit]

        # Combine all results
        all_items = list(chain(lernsets_qs, quizzes_qs, modules_qs, studiengaenge_qs))

        # Calculate relevance score for each item
        def calculate_relevance(item):
            words = query.lower().split()
            score = 0
            text_fields = []
            if isinstance(item, Lernset):
                text_fields = [item.title, item.description]
            elif isinstance(item, Quiz):
                text_fields = [item.title, item.description]
            elif isinstance(item, Modul):
                text_fields = [item.name, item.dozent_name or '', item.modulId]
            elif isinstance(item, Studiengang):
                text_fields = [item.name, item.description, item.id]


            for field in text_fields:
                if field:
                    field_lower = field.lower()
                    for word in words:
                        # Check for whole word match (higher score)
                        if re.search(r'\b' + re.escape(word) + r'\b', field_lower):
                            score += 2
                        elif word in field_lower:
                            score += 1
            return score

        # Sort by relevance score descending, then limit
        all_items.sort(key=calculate_relevance, reverse=True)
        all_items.sort(key=calculate_relevance, reverse=True)
        all_items = all_items[:limit]

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
    """
    API endpoint for suggesting quizzes to the user based on their field of study.
    Returns recent quizzes from modules in the user's study program.
    """
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
