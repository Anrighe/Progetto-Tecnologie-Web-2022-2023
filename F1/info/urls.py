from django.urls import path
from .models import *

from info.views import crispy, monaco_view, SessioniPageView, CircuitiView, ScuderiaView

app_name = 'info'

urlpatterns = [
    path('monaco/', monaco_view, name='monaco'),
    path('crispy/', crispy, name='crispy'),
    path('sessioni/', SessioniPageView.as_view(), name='sessioni'),
    path('circuiti/', CircuitiView.as_view(), name='circuiti'),
    path('scuderie/', ScuderiaView.as_view(), name='scuderie' )
]