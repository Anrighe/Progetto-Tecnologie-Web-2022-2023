from django.urls import path
from .models import *
from . import views

from media.views import crispy, HomePageView

app_name = 'media'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('news/', views.HomePageView.as_view(), name='news'),
    path('crispy/', crispy, name='crispy')
]
