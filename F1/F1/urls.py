"""
URL configuration for F1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from .views import UserCreateView

from .views import prova

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/images/icons/favicon.ico')),
    path('', include('media.urls')),
    path('admin/', admin.site.urls),
    path('prova/', prova, name='prova'),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path('', include('info.urls')),
]
