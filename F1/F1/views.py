from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.urls import reverse_lazy
from store.models import Utente, Gestore_Circuito, Carrello, Notifica, Ordine, TipologiaBiglietto, IstanzaBiglietto
from media.models import PortaleF1
from django.http import JsonResponse
import os


def UserCreateSelection(request):
    return render(request, template_name='registration/user_type_selection.html')


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('media:homepage')

    def form_valid(self, form):
        # Salva il model dell'istanza dell'User
        response = super().form_valid(form)

        portale_f1 = PortaleF1.objects.first()

        # Crea un'istanza di Utente e la connette al suo corrispettivo "User" e al "PortaleF1"
        utente = Utente.objects.create(user=self.object, portale_f1=portale_f1)

        username = self.object.username

        path = os.path.join(os.getcwd(), 'static', 'users', username)
        
        # Se esiste una cartella chiamata come l'utente nel percorso F1\static\users la elimina e poi la crea nuovamente
        if os.path.exists(path):
            os.remove(path)

        os.mkdir(path)

        # Crea un'istanza di Carrello e la connette al suo corrispettivo "Utente"
        Carrello.objects.create(possedimento_carrello=utente)

        return response
    

class CompanyCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/company_create.html'
    success_url = reverse_lazy('media:homepage')

    def form_valid(self, form):
        # Salva il model dell'istanza del gestore
        response = super().form_valid(form)

        portale_f1 = PortaleF1.objects.first()

        # Crea un'istanza di Gestore e la connette al suo corrispettivo "User" e al "PortaleF1"
        Gestore_Circuito.objects.create(user=self.object, portale_f1=portale_f1)

        username = self.object.username

        path = os.path.join(os.getcwd(), 'static', 'companies', username)

        #TODO: Trovare una soluzione nel caso la cartella esista già 
        # PermissionError: [WinError 5] Access is denied: 'C:\\Python\\Progetto-Tecnologie-Web-2022-2023\\F1\\static\\companies\\provagestore1'

        # Se esiste una cartella chiamata come il gestore nel percorso F1\static\users la elimina e poi la crea nuovamente
        if os.path.exists(path):
            os.remove(path)

        os.mkdir(path)

        return response
    

def nothing_here(request):
    return render(request, template_name='nothing_here.html')

def get_notifications(request):
    '''Ritorna le notifiche dell'utente loggato'''
    notifiche = None
    if request.user.is_authenticated:
        
        try:
            if request.user.utente:
                utente = True
                gestore = False
        except:
            utente = False
            gestore = True


        if utente:
            ordini_utente = Ordine.objects.filter(utente=request.user.utente)

            # Trova tutte le notifiche relative a ordini che fanno parte di ordini_utente
            data = Notifica.objects.filter(ordine__in=ordini_utente)
            notifiche = [{'id': notification.id, 'descrizione': notification.descrizione, 'order': notification.ordine.id} for notification in data]

        elif gestore:

            gestore_circuito = Gestore_Circuito.objects.get(user=request.user)

            tipologie_biglietti = TipologiaBiglietto.objects.filter(gestore_circuito=gestore_circuito)
            istanze_biglietti = IstanzaBiglietto.objects.filter(tipologia_biglietto__in=tipologie_biglietti, ordine__isnull=False).distinct()

            ordini = []
            for biglietto in istanze_biglietti:
                ordini.append(biglietto.ordine)

            notifiche = Notifica.objects.filter(ordine__in=ordini)

            print(notifiche)
            notifiche = [{'id': notification.id, 'descrizione': notification.descrizione, 'order': notification.ordine.id} for notification in notifiche]

    return JsonResponse(notifiche, safe=False)

    