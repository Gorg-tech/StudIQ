"""
REST URL Routers for quiz-related requests.

This file defines the URLs for the REST API and which views to call.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import QuizViewSet, QuestionViewSet, LernsetViewSet, QuizAttemptViewSet, QuizSessionViewSet,\
                    FeedbackViewSet, StudiengangViewSet, ModulViewSet, SearchView,\
                    AnswerOptionViewSet, SuggestedQuizzesView
from .views import LeaderboardViewSet

router = DefaultRouter()
router.register(r'modules', ModulViewSet, basename='modules')
router.register(r'lernsets', LernsetViewSet, basename='lernsets')
router.register(r'quizzes', QuizViewSet, basename='quizzes')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'attempts', QuizAttemptViewSet, basename='attempts')
router.register(r'sessions', QuizSessionViewSet, basename='sessions')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'studiengaenge', StudiengangViewSet)
router.register(r'module', ModulViewSet)
router.register(r'answer-options', AnswerOptionViewSet)
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    path('suggested-quizzes/', SuggestedQuizzesView.as_view(), name='suggested-quizzes'),
    path('', include(router.urls)),

    # Brauchen wir erstmal nicht
    # Nested: /api/module/<module_id>/lernsets/
    # path('modules/<int:module_id>/lernsets/', views.LernsetsByModuleView.as_view(),
    #      name='module-lernsets'),
    # Nested: /api/lernsets/<int:lernset_id>/quizzes/
    path('lernsets/<uuid:lernset_id>/quizzes/', views.QuizzesByLernsetView.as_view(),
         name='lernset-quizzes'),
    path('search/', SearchView.as_view(), name='search'),
    path('quizzes/<uuid:quiz_id>/complete/', views.QuizCompletionView.as_view(), name='complete'),
]
