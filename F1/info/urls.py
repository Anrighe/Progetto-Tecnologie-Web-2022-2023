from django.urls import path
from .models import *

from info.views import monaco_view, SessioniView, CircuitiView, ScuderieView, RisultatoSessioneView, TeamView, PilotaView, CircuitoView

app_name = 'info'

urlpatterns = [
    path('monaco/', monaco_view, name='monaco'),
    path('sessioni/', SessioniView.as_view(), name='sessioni'),
    path('sessioni/<pk>/<tipo_sessione>/', RisultatoSessioneView.as_view(), name='risultato_sessione'),
    path('circuiti/', CircuitiView.as_view(), name='circuiti'),
    path('circuiti/<pk>/', CircuitoView.as_view(), name='circuito'),
    path('scuderie/', ScuderieView.as_view(), name='scuderie' ),
    path('scuderie/<pk>/', TeamView.as_view(), name='team'),
    path('pilota/<pk>/', PilotaView.as_view(), name='pilota'),
]