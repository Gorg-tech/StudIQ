from django.urls import path

from .views import RegisterView, LoginView, LogoutView, MeView, csrf, UserStatsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('me/stats/', UserStatsView.as_view(), name='me-stats'),
    path('csrf/', csrf, name='csrf'), 
]
