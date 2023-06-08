from django.urls import path
from .models import *

from info.views import crispy, monaco_view, SessioniView, CircuitiView, ScuderiaView, RisultatoSessioneView

app_name = 'info'

urlpatterns = [
    path('monaco/', monaco_view, name='monaco'),
    path('crispy/', crispy, name='crispy'),
    path('sessioni/', SessioniView.as_view(), name='sessioni'),
    path('sessioni/<pk>/<tipo_sessione>/', RisultatoSessioneView.as_view(), name='risultato_sessione'),
    path('circuiti/', CircuitiView.as_view(), name='circuiti'),
    path('scuderie/', ScuderiaView.as_view(), name='scuderie' )
]