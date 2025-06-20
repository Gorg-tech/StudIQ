from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, LernsetViewSet, QuizProgressViewSet, AchievementViewSet, QuizSessionViewSet, FeedbackViewSet, StudiengangViewSet, ModulViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'lernsets', LernsetViewSet)
router.register(r'progress', QuizProgressViewSet, basename='progress')
router.register(r'achievements', AchievementViewSet)
router.register(r'sessions', QuizSessionViewSet, basename='sessions')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'studiengaenge', StudiengangViewSet)
router.register(r'module', ModulViewSet)

urlpatterns = [
    path('', include(router.urls)),
]