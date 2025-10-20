from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import QuizViewSet, QuestionViewSet, LernsetViewSet, QuizProgressViewSet, AchievementViewSet, QuizSessionViewSet, FeedbackViewSet, StudiengangViewSet, ModulViewSet, SearchView, AnswerOptionViewSet

router = DefaultRouter()
router.register(r'modules', ModulViewSet, basename='modules')
router.register(r'lernsets', LernsetViewSet, basename='lernsets')
router.register(r'quizzes', QuizViewSet, basename='quizzes')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'achievements', AchievementViewSet)
router.register(r'sessions', QuizSessionViewSet, basename='sessions')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'studiengaenge', StudiengangViewSet)
router.register(r'module', ModulViewSet)
router.register(r'answer-options', AnswerOptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Brauchen wir erstmal nicht
    # Nested: /api/module/<module_id>/lernsets/
    # path('modules/<int:module_id>/lernsets/', views.LernsetsByModuleView.as_view(), name='module-lernsets'),
    # Nested: /api/lernsets/<int:lernset_id>/quizzes/
    path('lernsets/<uuid:lernset_id>/quizzes/', views.QuizzesByLernsetView.as_view(), name='lernset-quizzes'),
    # Add the new search endpoint
    path('search/', SearchView.as_view(), name='search'),
]
