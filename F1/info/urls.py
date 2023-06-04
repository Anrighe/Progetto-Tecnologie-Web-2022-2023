from django.urls import path
from .models import *

from info.views import crispy, monaco_view, SessioniPageView

app_name = 'info'

urlpatterns = [
    path('monaco/', monaco_view, name='monaco'),
    path('crispy/', crispy, name='crispy'),
    path('sessioni/', SessioniPageView.as_view(), name='sessioni'),
]