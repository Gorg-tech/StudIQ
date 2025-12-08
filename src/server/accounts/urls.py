"""
REST URL Routers for account-related requests.

This file defines the URLs for the REST API and which views to call.
"""

from django.urls import path

from .views import RegisterView, LoginView, LogoutView, MeView, csrf, UserStatsView,\
                    StudyCalendarView, FriendRequestsView, FriendsListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('me/stats/', UserStatsView.as_view(), name='me-stats'),
    path('me/streaks/', StudyCalendarView.as_view(), name='me-streaks'),
    path('me/friend-requests/', FriendRequestsView.as_view(), name='me-friend-requests'),
    path('me/friends/', FriendsListView.as_view(), name='me-friends'),
    path('csrf/', csrf, name='csrf'),
]
