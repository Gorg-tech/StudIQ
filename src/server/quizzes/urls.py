from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, LernsetViewSet, QuizProgressViewSet, AchievementViewSet, QuizSessionViewSet, FeedbackViewSet, StudiengangViewSet, ModulViewSet
from .views import LernsetsByModuleView, QuizzesByLernsetView, QuestionsByQuizView


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

urlpatterns = [
    path('', include(router.urls)),
    # Nested: /api/module/<module_id>/lernsets/
    path('modules/<int:module_id>/lernsets/', views.LernsetsByModuleView.as_view(), name='module-lernsets'),
    # Nested: /api/lernsets/<int:lernset_id>/quizzes/
    path('lernsets/<int:lernset_id>/quizzes/', views.QuizzesByLernsetView.as_view(), name='lernset-quizzes'),
    # Nested: /api/quizzes/<int:quiz_id>/questions/
    path('quizzes/<int:quiz_id>/questions/', views.QuestionsByQuizView.as_view(), name='quiz-questions'),
]