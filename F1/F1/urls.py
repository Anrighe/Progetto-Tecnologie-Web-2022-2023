from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from .views import UserCreateView, nothing_here, UserCreateSelection, CompanyCreateView, get_notifications

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/images/icons/favicon.ico')),
    path('admin/', admin.site.urls),
    path('nothing_here/', nothing_here, name='nothing_here'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', UserCreateSelection, name='register_selection'),
    path('register/utente/', UserCreateView.as_view(), name='register_user'),
    path('register/gestore/', CompanyCreateView.as_view(), name='register_company'),
    path('', include('media.urls')),
    path('', include('info.urls')),
    path('', include('store.urls')),
    path('query/notifications/', get_notifications, name='get_notifications'),
]
