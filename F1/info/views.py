from django.views.generic.list import ListView
from info.models import Circuito, Partecipazione, Scuderia, Sessione, Pilota

from media.forms import FormUtente

from django.shortcuts import get_object_or_404, render

def crispy(request):
    context = {'form': FormUtente()}
    return render(request, 'media/crispy.html', context)


def monaco_view(request):
    ctx = {"obj": get_object_or_404(Circuito, nome='Circuit de Monaco')}
    return render(request, template_name='info/circuito.html', context=ctx)


class CircuitiView(ListView):
    model = Circuito
    template_name = 'info/menu_circuito.html' 

    def get_queryset(self):
        return self.model.objects.filter(nome="Circuit de Monaco")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = Circuito.objects.all()
        context['query'] = query
        return context


class ScuderiaView(ListView):
    model = Scuderia
    template_name = 'info/scuderia.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scuderie = Scuderia.objects.all().order_by('-punti')
        piloti = Pilota.objects.all()

        context['piloti'] = piloti
        context['scuderie'] = scuderie
        
        return context


class SessioniView(ListView):
    model = Partecipazione
    template_name = 'info/sessioni.html' 

    def get_context_data(self):
        context = super().get_context_data()

        circuiti = Circuito.objects.all()
        context['circuiti'] = circuiti

        partecipazioni = Partecipazione.objects.filter(posizione=1, sessione__tipo='gara').order_by('-data')
        context['partecipazioni'] = partecipazioni
        
        return context
    

class RisultatoSessioneView(ListView):
    model = Partecipazione
    template_name = 'info/risultato_sessione.html' 

    #TODO: implementare il sistema dei punti
    #The winner receives 25 points, the second-place finisher 18 points, 
    # with 15, 12, 10, 8, 6, 4, 2 and 1 points for positions 
    # 3 through 10, respectively. One additional point is awarded 
    # to the driver and team with the fastest lap of the race, 
    # but only if this driver finishes in the top 10 positions.

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        pk = self.kwargs.get('pk')
        tipo_sessione = self.kwargs.get('tipo_sessione')
        partecipazioni = Partecipazione.objects.filter(circuito__pk=pk, sessione__tipo=tipo_sessione).order_by('posizione')
        sessioni_effettuate = Partecipazione.objects.filter(circuito__pk=pk).values_list('sessione__tipo', flat=True).distinct()
        
        context['partecipazioni'] = partecipazioni
        context['sessioni_effettuate'] = sessioni_effettuate
        context['pk'] = pk
        
        return context