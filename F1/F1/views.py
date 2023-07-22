from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.urls import reverse_lazy
from store.models import Utente, Gestore_Circuito
from media.models import PortaleF1
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
        Utente.objects.create(user=self.object, portale_f1=portale_f1)

        username = self.object.username

        path = os.path.join(os.getcwd(), 'static', 'users', username)
        
        # Se esiste una cartella chiamata come l'utente nel percorso F1\static\users la elimina e poi la crea nuovamente
        if os.path.exists(path):
            os.remove(path)

        os.mkdir(path)

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

    