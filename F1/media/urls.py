from django.urls import path
from .models import *
from . import views

from media.views import crispy





app_name = 'media'

urlpatterns = [
    path('news/', views.HomePageView.as_view(), name='news'),
    path('crispy/', crispy, name='crispy')
]
