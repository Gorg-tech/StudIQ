"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from quizzes.views import csrf, login_view   # CSRF‑ und Login‑Views aus der App

urlpatterns = [
    path('admin/', admin.site.urls),

    # Öffentliche Auth‑ und CSRF‑Endpunkte
    path('api/csrf/',  csrf,       name='api-csrf'),
    path('api/login/', login_view, name='api-login'),

    # Accounts‑Routen (bleiben unverändert)
    path('api/auth/',  include('accounts.urls')),
    path('api/users/', include('accounts.urls')),

    # Alle übrigen Quiz‑API‑Endpunkte
    path('api/', include('quizzes.urls')),
]
