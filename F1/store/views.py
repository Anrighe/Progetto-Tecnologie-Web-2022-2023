from typing import Any, Dict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from store.models import Utente, TipologiaBiglietto, IstanzaBiglietto, Carrello
from django.core.files.storage import FileSystemStorage
import os
from PIL import Image
from django.contrib import messages
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
import re
from datetime import date
from store.forms import UserProfileFormData, TicketForm
from django.core.paginator import Paginator, EmptyPage



# Classe che gestisce la modifica dei dati dell'utente
class UserProfileDataChangeViewUpdate(LoginRequiredMixin, UpdateView):
    model = Utente
    template_name = 'store/user_profile_data_change.html'
    success_url = '/store/profile/'
    form_error_messages = ''

    user_data_form = UserProfileFormData()

    def get_form(self, form_class=None):

        user = Utente.objects.filter(user=self.request.user)

        initial_data = {
            'nome': self.request.user.first_name,
            'cognome': self.request.user.last_name,
            'email': self.request.user.email,
            'indirizzo': user[0].indirizzo,
            'data_nascita': user[0].data_nascita,
            'sesso': user[0].sesso,
            'paese': user[0].paese,
            'telefono': user[0].telefono,
            'carta_credito': user[0].carta_credito,
            'cvv': user[0].cvv,
            'scadenza_carta': user[0].scadenza_carta,
        }

        self.user_data_form = UserProfileFormData(initial=initial_data)        

        return self.user_data_form
    
    def get_object(self):
        return get_object_or_404(Utente, user=self.request.user)

    def post(self, request, *args, **kwargs):
        # Recupera e aggiorna l'istanza utente e user
        self.form_error_messages = ''
        utente = self.get_object()
        
        if self.are_inputs_correct():

            utente.user.first_name = request.POST.get('nome')
            utente.user.last_name = request.POST.get('cognome')
            utente.user.email = request.POST.get('email')
                    
            utente.indirizzo = request.POST.get('indirizzo')
            utente.data_nascita = request.POST.get('data_nascita')
            utente.sesso = request.POST.get('sesso')
            utente.paese = request.POST.get('paese')
            print(request.POST.get('paese'))
            utente.telefono = request.POST.get('telefono')
            utente.carta_credito = request.POST.get('carta_credito')
            utente.cvv = request.POST.get('cvv')
            utente.scadenza_carta = request.POST.get('scadenza_carta')
            
            utente.save()
            utente.user.save()

            messages.success(request, 'Dati del profilo salvati con successo')
            return redirect('store:profile')
        else:
            messages.error(request, self.form_error_messages)
            return redirect('store:profile')
    
    def are_inputs_correct(self):
        check_function_list = [
            self.check_first_name,
            self.check_last_name,
            self.check_email,
            self.check_data_nascita,
            self.check_telefono,
            self.check_carta_credito,
            self.check_scadenza_carta,
            self.check_cvv
        ]
        for check_function in check_function_list:
            check_function()

        if self.form_error_messages == '':
            return True
        else:
            return False
              
    def check_first_name(self):
        if not (self.request.POST.get('nome').isalpha() or self.request.POST.get('nome') == ''):
            self.form_error_messages = f'{self.form_error_messages}- Il nome non può contenere numeri o caratteri speciali'

    def check_last_name(self):
        if not (self.request.POST.get('cognome').isalpha() or self.request.POST.get('nome') == ''):
            self.form_error_messages = f'{self.form_error_messages}- Il cognome non può contenere numeri o caratteri speciali'

    def check_email(self):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', self.request.POST.get('email')):
            self.form_error_messages = f'{self.form_error_messages}- L\'email inserita non è valida'
    
    def check_data_nascita(self):
        if self.request.POST.get('data_nascita'):
            try:
                data_nascita = date.fromisoformat(self.request.POST.get('data_nascita'))
                if data_nascita > date.today():
                    self.form_error_messages = f'{self.form_error_messages}- La data di nascita non può essere nel futuro'
            except ValueError:
                self.form_error_messages = f'{self.form_error_messages}- La data di nascita inserita non è valida'

    def check_telefono(self):
        if not re.match(r'^\+?[0-9]{7,12}$', self.request.POST.get('telefono')):
            self.form_error_messages = f'{self.form_error_messages}- Il numero di telefono inserito non è valido'

    def check_carta_credito(self):
        if not re.match(r'^[0-9]{10,19}$', self.request.POST.get('carta_credito')):
            self.form_error_messages = f'{self.form_error_messages}- Il numero di carta di credito inserito non è valido'

    def check_scadenza_carta(self):
        if self.request.POST.get('scadenza_carta'):
            try:
                data_nascita = date.fromisoformat(self.request.POST.get('scadenza_carta'))
                if data_nascita < date.today():
                    self.form_error_messages = f'{self.form_error_messages}- La carta è scaduta'
            except ValueError:
                self.form_error_messages = f'{self.form_error_messages}- La data inserita di scadenza della carta non è valida'

    def check_cvv(self):
        if not re.match(r'^[0-9]{3}$', self.request.POST.get('cvv')):
            self.form_error_messages = f'{self.form_error_messages}- Il CVV non è valido'


@login_required
def UserProfile(request):
    ALLOWED_IMAGE_FORMATS = ['JPEG', 'JPG', 'PNG']
    user = request.user

    try:
        utente = Utente.objects.get(user=user)

        # Caricamento di una nuova immagine profilo
        if request.method == 'POST':

            uploaded_file = request.FILES.get('profile-image-file')
            
            # Se è stato effettivamente selezionato e caricato un file 
            if uploaded_file:
                try:
                    image = Image.open(uploaded_file)

                    if image.format in ALLOWED_IMAGE_FORMATS:

                        username = user.username
                        
                        path = os.path.join(os.getcwd(), 'static', 'users', username)

                        # Cancella i file precedentemente presenti nella cartella dell'utente
                        for file_name in os.listdir(path):
                            file_path = os.path.join(path, file_name)
                            if os.path.isfile(file_path):
                                os.remove(file_path)

                        fs = FileSystemStorage(location=path)

                        filename = fs.save(uploaded_file.name, uploaded_file)
                        
                        utente.immagine_profilo = f'/static/users/{username}/{filename}'
                        utente.save()
                    else:
                        messages.error(request, 'Formato dell\'immagine non valido. Utilizza un file in formato JPEG, JPG, o PNG.')
                except Image.UnidentifiedImageError:
                    print('UnidentifiedImageError')
                    messages.error(request, 'Il file caricato non sembra essere un\'immagine. Utilizza un file in formato JPEG, JPG, o PNG.')
            else:
                messages.error(request, 'Non è stata caricata nessuna immagine.')

    except Utente.DoesNotExist:
        utente = None

    ctx = {'utente': utente}

    return render(request, 'store/user_profile.html', ctx)    


class StoreView(ListView):
    model = TipologiaBiglietto
    template_name = 'store/store.html'
    NUM_BIGLIETTI_PER_PAGINA = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tipologie_biglietti = TipologiaBiglietto.objects.all().order_by('-data_evento')

        istanze_biglietti = IstanzaBiglietto.objects.all()

        # Aggiunge il conteggio delle istanze di una tipologia per ogni tipologia di prodotto
        for tipologia_biglietto in tipologie_biglietti:
            tipologia_biglietto.amount = tipologia_biglietto.get_istanza_biglietto_amount()

        context['istanze_biglietti'] = istanze_biglietti

        paginator = Paginator(tipologie_biglietti, StoreView.NUM_BIGLIETTI_PER_PAGINA)
        numero_pagina = self.request.GET.get('page', 1)
        pagina = paginator.page(numero_pagina)

        context['tipologie_biglietti'] = pagina

        return context
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except EmptyPage:
            return redirect('nothing_here')
    
class ProductView(ListView):
    model = TipologiaBiglietto
    template_name = 'store/product.html'
    user_data_form = TicketForm()

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk') # Contiene l'id della tipologia del biglietto selezionato

        tipologia_biglietto = TipologiaBiglietto.objects.get(pk=pk)

        istanze_biglietti = IstanzaBiglietto.objects.filter(tipologia_biglietto=tipologia_biglietto)
        
        context['form'] = TicketForm()
        context['form'].fields['istanze_biglietti'].choices = [(istanza_biglietto.pk, istanza_biglietto.numero_posto) for istanza_biglietto in istanze_biglietti]

        context['tipologia_biglietto'] = tipologia_biglietto

        context['istanze_biglietti'] = istanze_biglietti

        return context
    
    
    @method_decorator(login_required(login_url='/login/?auth=notok'))
    def post(self, request, *args, **kwargs):
        '''Aggiunge un biglietto al carrello dell'utente'''
        user_pk = request.user.pk
        utente_pk = Utente.objects.get(user=request.user)
        carrello_utente = Carrello.objects.get(possedimento_carrello=utente_pk)
        istanza_biglietto_selezionato = IstanzaBiglietto.objects.get(pk=request.POST.get('istanze_biglietti'))

        carrello_utente.istanze_biglietti.add(istanza_biglietto_selezionato)

        return redirect('store:product', pk=kwargs['pk'])
    
class CartView(LoginRequiredMixin, ListView):
    model = Carrello
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        utente = Utente.objects.get(user=self.request.user)
        carrello_utente = Carrello.objects.get(possedimento_carrello=utente)
        remove = self.request.GET.get('remove')
        if remove:
            carrello_utente.istanze_biglietti.remove(IstanzaBiglietto.objects.get(pk=remove))
            print(remove)

        biglietti_carrello = carrello_utente.istanze_biglietti.all()

        context['utente'] = utente
        context['carrello_utente'] = carrello_utente
        context['biglietti_carrello'] = biglietti_carrello
        context['totale_biglietti'] = carrello_utente.istanze_biglietti.all().count()

        return context
    
