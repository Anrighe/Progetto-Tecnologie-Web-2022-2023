from django.views.generic.list import ListView
from info.models import Circuito, Partecipazione, Scuderia, Sessione, Pilota

from media.forms import FormUtente
from store.models import Utente

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


class CircuitiView(ListView):
    '''Gestisce la pagina dei circuiti, mostrando i circuiti in ordine di data di evento'''
    model = Circuito
    template_name = 'info/menu_circuito.html' 

    def get_queryset(self):
        return self.model.objects.filter(nome="Circuit de Monaco")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        circuiti = Circuito.objects.all().order_by('-data_evento')
        context['circuiti'] = circuiti
        return context
    

class CircuitoView(ListView):
    '''Gestisce la pagina di un specifico circuito, mostrando le informazioni relative ad esso'''
    model = Circuito
    template_name = 'info/circuito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        circuito = Circuito.objects.get(pk=pk)

        context['circuito'] = circuito
        return context


class ScuderieView(ListView):
    '''Gestisce la pagina delle scuderie, mostrando le scuderie in ordine di punti'''
    model = Scuderia
    template_name = 'info/scuderia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scuderie = Scuderia.objects.all().order_by('-punti')
        piloti = Pilota.objects.all()

        context['piloti'] = piloti
        context['scuderie'] = scuderie
        
        return context
    

class TeamView(ListView):
    '''Gestisce la pagina di una specifica scuderia, mostrando le informazioni relative ad essa'''
    model = Scuderia
    template_name = 'info/team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        scuderia = Scuderia.objects.get(pk=pk)
        piloti = Pilota.objects.all()

        context['scuderia'] = scuderia
        context['piloti'] = piloti
        context['pk'] = pk

        try:
            context['follow'] = False
            if self.request.user.is_authenticated:
                utente = Utente.objects.get(user=self.request.user)
                if scuderia in utente.follow.all():
                    context['follow'] = True
                    
        except Utente.DoesNotExist:
            return context
        
        return context
    

class PilotaView(ListView):
    '''Gestisce la pagina di un specifico pilota, mostrando le informazioni relative ad esso'''
    model = Pilota
    template_name = 'info/pilota.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        pilota = Pilota.objects.get(pk=pk)

        context['pilota'] = pilota
        return context



class SessioniView(ListView):
    '''Gestisce la pagina delle sessioni, mostrando le sessioni in ordine di data'''
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
    '''Gestisce la pagina dei risultati di una specifica sessione, mostrando le informazioni relative ad essa'''
    model = Partecipazione
    template_name = 'info/risultato_sessione.html' 
    
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

@login_required
def follow(request, **kwargs):
    '''
    Aggiunge una scuderia alla lista dei preferiti dell'utente corrente e, se l'utente non è autenticato, 
    viene reindirizzato alla pagina di login.
    Valido solamente per gli utenti -> nel caso in cui un gestore provi ad accedere a questa view,
    verrebbe reindirizzato alla pagina della scuderia senza alcuna modifica al suo stato
    '''
    pk = kwargs.get('pk')
    if request.user.is_authenticated:
        try:
            utente = Utente.objects.get(user=request.user)
            scuderia = Scuderia.objects.get(pk=pk)

            if scuderia:
                utente.follow.add(scuderia)
                utente.save()
        except Utente.DoesNotExist:
            return redirect('info:team', pk=pk)

    return redirect('info:team', pk=pk)

@login_required
def unfollow(request, **kwargs):
    '''
    Rimuove una scuderia alla lista dei preferiti dell'utente corrente, e se l'utente non è autenticato,
    viene reindirizzato alla pagina di login.
    Valido solamente per gli utenti -> nel caso in cui un gestore provi ad accedere a questa view,
    verrebbe reindirizzato alla pagina della scuderia senza alcuna modifica al suo stato
    '''
    pk = kwargs.get('pk')
    if request.user.is_authenticated:
        try:
            utente = Utente.objects.get(user=request.user)
            scuderia = Scuderia.objects.get(pk=pk)

            if scuderia:
                utente.follow.remove(scuderia)
                utente.save()
        except Utente.DoesNotExist:
            return redirect('info:team', pk=pk)

    return redirect('info:team', pk=pk)