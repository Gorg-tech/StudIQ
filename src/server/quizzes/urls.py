
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    QuizViewSet,
    QuestionViewSet,
    LernsetViewSet,
    QuizProgressViewSet,
    AchievementViewSet,
    QuizSessionViewSet,
    FeedbackViewSet,
    StudiengangViewSet,
    ModulViewSet,
    LernsetsByModuleView,
    QuizzesByLernsetView,
    QuestionsByQuizView,
)

router = DefaultRouter()
router.register(r'modules', ModulViewSet, basename='module')
router.register(r'lernsets', LernsetViewSet, basename='lernset')
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'sessions', QuizSessionViewSet, basename='session')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'studiengaenge', StudiengangViewSet, basename='studiengang')

urlpatterns = [
    # alle automatisch vom Router erzeugten Endpunkte
    *router.urls,

    # verschachtelte Hilfs-Endpunkte
    path('modules/<int:module_id>/lernsets/', LernsetsByModuleView.as_view(), name='module-lernsets'),
    path('lernsets/<int:lernset_id>/quizzes/', QuizzesByLernsetView.as_view(), name='lernset-quizzes'),
    path('quizzes/<int:quiz_id>/questions/', QuestionsByQuizView.as_view(), name='quiz-questions'),
]
