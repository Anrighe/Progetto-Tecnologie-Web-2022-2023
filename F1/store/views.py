from typing import Any, Dict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from store.models import Utente, TipologiaBiglietto, IstanzaBiglietto, Carrello, Ordine, Gestore_Circuito, Notifica
from django.core.files.storage import FileSystemStorage
import os
from PIL import Image
from django.contrib import messages
from django.views.generic import UpdateView, CreateView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from django.core.exceptions import ValidationError
import re
from django.utils import timezone
from datetime import date, timedelta
from store.forms import UtenteProfileFormData, TicketForm, GestoreProfileFormData, CreateTicketTypeForm, CreateTicketInstanceForm
from django.core.paginator import Paginator, EmptyPage
from store.ticket_generator import generate_ticket



class UtenteProfileDataChangeViewUpdate(LoginRequiredMixin, UpdateView):
    '''Classe che gestisce la pagina di modifica dei dati dell'utente'''
    model = Utente
    template_name = 'store/user_profile_data_change.html'
    success_url = '/store/profile/'
    form_error_messages = ''

    user_data_form = UtenteProfileFormData()
    

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

        self.user_data_form = UtenteProfileFormData(initial=initial_data)        

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
        if not (self.request.POST.get('cognome').isalpha() or self.request.POST.get('cognome') == ''):
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
            if not self.request.POST.get('carta_credito') == '':
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
            if not self.request.POST.get('cvv') == '':
                self.form_error_messages = f'{self.form_error_messages}- Il CVV non è valido'


@login_required
def UserProfile(request):
    '''Gestisce la pagina del profilo dell'utente'''
    ALLOWED_IMAGE_FORMATS = ['JPEG', 'JPG', 'PNG']
    user = request.user

    utente = False
    gestore = False
    try:
        if user.gestore_circuito:
            gestore = True
    except Exception as e:
        print('The current user is an Utente type')

    try:
        if user.utente:
            utente = True
    except Exception as e:
        print('The current user is a Gestore_Circuito type')

    try:
        if gestore:
            # Imposta il booleano delle notifiche a False
            user.gestore_circuito.notifiche = False
            user.gestore_circuito.save()

            gestore_circuito = Gestore_Circuito.objects.get(user=user)
            circuito = user.gestore_circuito.gestione_circuito

            ordini_totali = Ordine.objects.filter(utente__isnull=False).order_by('-data')
            istanze_biglietti_venduti = IstanzaBiglietto.objects.filter()

            # Contiene tutti gli ordini di biglietti per il circuito gestito dal gestore corrente
            ordini_circuito = ordini_totali.filter(istanzabiglietto__tipologia_biglietto__gestore_circuito=gestore_circuito).distinct().order_by('-id')

            # Crea un dizionario con chiave l'offset in giorni rispetto alla data odierna e come valore una tupla per il numero di biglietti venduti per settore
            # Esempio: -7: (1, 2, 5) --> 7 giorni fa sono stati venduti 1 biglietto per il settore 1, 2 biglietti per il settore 2 e 5 biglietti per il settore 3
            orders_by_day = { offset: (0, 0, 0) for offset in range(-6, 1) }

            for offset in range(-7, 1):
                ordini = ordini_circuito.filter(data=timezone.now() + timedelta(days=offset)).distinct()
                settore1 = 0
                settore2 = 0
                settore3 = 0
                for ordine in ordini:

                    for biglietto in istanze_biglietti_venduti:

                        if biglietto.ordine == ordine:

                            match biglietto.tipologia_biglietto.settore:
                                case '1':
                                    settore1 += 1
                                case '2':
                                    settore2 += 1
                                case '3':
                                    settore3 += 1
                                case _:
                                    pass

                orders_by_day[offset] = (settore1, settore2, settore3)

            ctx = {
                'utente': user.gestore_circuito, 
                'circuito': circuito, 
                'ordini_circuito': ordini_circuito,
                '7d': orders_by_day[-7],
                '6d': orders_by_day[-6],
                '5d': orders_by_day[-5],
                '4d': orders_by_day[-4],
                '3d': orders_by_day[-3],
                '2d': orders_by_day[-2],
                '1d': orders_by_day[-1],
                '0d': orders_by_day[0],

            }
            return render(request, 'store/user_profile.html', ctx)
        
        elif utente:
            # Imposta il booleano delle notifiche a False
            user.utente.notifiche = False
            user.utente.save()

            utente = Utente.objects.get(user=user)
            ordini_utente = Ordine.objects.filter(utente=utente).order_by('-id')

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
                        messages.error(request, 'Il file caricato non sembra essere un\'immagine. Utilizza un file in formato JPEG, JPG, o PNG.')
                else:
                    messages.error(request, 'Non è stata caricata nessuna immagine.')

    except Utente.DoesNotExist:
        utente = None

    ctx = {'utente': utente, 'ordini_utente': ordini_utente}

    return render(request, 'store/user_profile.html', ctx)    


class StoreView(ListView):
    '''Classe che gestisce la pagina dello store'''
    model = TipologiaBiglietto
    template_name = 'store/store.html'
    NUM_BIGLIETTI_PER_PAGINA = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print(kwargs)
        filter = None
        try:
            filter = self.request.GET.get('filter')
            print("FILTER:", filter)
        except Exception as e:
            print("EXCEPTION:", e)
        
        match filter:
            case 'price_asc':
                #hide tipologia biglietto tickets where instance.order is not null
                
                tipologie_biglietti = TipologiaBiglietto.objects.all().order_by('prezzo')
            case 'price_desc':
                tipologie_biglietti = TipologiaBiglietto.objects.all().order_by('-prezzo')
            case 'date_asc':
                tipologie_biglietti = TipologiaBiglietto.objects.all().order_by('data_evento')
            case 'date_desc':
                tipologie_biglietti = TipologiaBiglietto.objects.all().order_by('-data_evento')
            case _:
                tipologie_biglietti = TipologiaBiglietto.objects.all().order_by('-data_evento')

        istanze_biglietti = IstanzaBiglietto.objects.filter(ordine=None)

        paginator = Paginator(tipologie_biglietti, StoreView.NUM_BIGLIETTI_PER_PAGINA)
        
        # Aggiunge il conteggio delle istanze di una tipologia per ogni tipologia di prodotto
        for tipologia_biglietto in tipologie_biglietti:
            tipologia_biglietto.amount = tipologia_biglietto.get_istanza_biglietto_amount()

        context['istanze_biglietti'] = istanze_biglietti

        numero_pagina = self.request.GET.get('page', 1)
        pagina = paginator.page(numero_pagina)

        context['tipologie_biglietti'] = pagina

        context['filter'] = filter

        return context
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except EmptyPage:
            return redirect('nothing_here')
    
class ProductView(ListView):
    '''Classe che gestisce la pagina di un prodotto'''
    model = TipologiaBiglietto
    template_name = 'store/product.html'
    user_data_form = TicketForm()

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk') # Contiene l'id della tipologia del biglietto selezionato

        tipologia_biglietto = TipologiaBiglietto.objects.get(pk=pk)

        istanze_biglietti = IstanzaBiglietto.objects.filter(tipologia_biglietto=tipologia_biglietto, ordine=None)
        
        context['form'] = TicketForm()
        context['form'].fields['istanze_biglietti'].choices = [(istanza_biglietto.pk, istanza_biglietto.numero_posto) for istanza_biglietto in istanze_biglietti]

        context['tipologia_biglietto'] = tipologia_biglietto

        context['istanze_biglietti'] = istanze_biglietti

        context['istanze_biglietti_amount'] = tipologia_biglietto.get_istanza_biglietto_amount()

        addproduct = self.request.GET.get('addproduct')
        if addproduct:
            context['addproduct'] = addproduct

        return context
    
    
    @method_decorator(login_required(login_url='/login/?auth=notok'))
    def post(self, request, *args, **kwargs):
        '''Aggiunge un biglietto al carrello dell'utente'''
        try:
            istanza_biglietto_selezionato = IstanzaBiglietto.objects.get(pk=request.POST.get('istanze_biglietti'))
            tipologia_biglietto_selezionato = istanza_biglietto_selezionato.tipologia_biglietto

            user_pk = request.user.pk
            utente_pk = Utente.objects.get(user=request.user)
            carrello_utente = Carrello.objects.get(possedimento_carrello=utente_pk)

            carrello_utente.istanze_biglietti.add(istanza_biglietto_selezionato)

        except Utente.DoesNotExist:
            return redirect('store:product', pk=tipologia_biglietto_selezionato.id)
        
        return redirect(reverse('store:product', kwargs=kwargs) + '?addproduct=ok')
    
class CartView(LoginRequiredMixin, ListView):
    '''Classe che gestisce il carrello dell'utente'''
    model = Carrello
    template_name = 'store/cart.html'
    IVA = 0.22

    def get_context_data(self, **kwargs):
        '''Recupera il carrello dell'utente e i biglietti presenti nel carrello, calcola il costo totale dei prodotti, le tasse e il costo totale tassato'''
        context = super().get_context_data(**kwargs)
        
        utente = Utente.objects.get(user=self.request.user)
        carrello_utente = Carrello.objects.get(possedimento_carrello=utente)
        
        remove = self.request.GET.get('remove')
        if remove:
            carrello_utente.istanze_biglietti.remove(IstanzaBiglietto.objects.get(pk=remove))

        purchase = self.request.GET.get('purchase')
        if purchase:
            context['purchase'] = purchase   

        error = self.request.GET.get('error')
        if error:
            error.replace('%20', ' ')
            context['error'] = error 

        biglietti_carrello = carrello_utente.istanze_biglietti.all()

        costo_totale_prodotti = 0
        tasse = 0
        costo_totale_prodotti_tasse = 0
        for biglietto in biglietti_carrello:
            costo_totale_prodotti += biglietto.tipologia_biglietto.prezzo

        tasse = costo_totale_prodotti * CartView.IVA
        costo_totale_prodotti_tasse = costo_totale_prodotti + tasse
        
        context['utente'] = utente
        context['carrello_utente'] = carrello_utente
        context['biglietti_carrello'] = biglietti_carrello
        context['totale_biglietti'] = carrello_utente.istanze_biglietti.all().count()
        context['costo_totale_prodotti'] = costo_totale_prodotti
        context['tasse'] = tasse
        context['costo_totale_prodotti_tasse'] = costo_totale_prodotti_tasse

        return context
    

    @method_decorator(login_required(login_url='/login/?auth=notok'))
    def post(self, request, *args, **kwargs):
        '''Controlla i dati dell'utente e se sono corretti crea un ordine, collegando tutti i prodotti acquistati a quell'ordine'''

        user = self.request.user 
        utente = Utente.objects.get(user=user)
        carrello_utente = Carrello.objects.get(possedimento_carrello=utente)
        biglietti_carrello = carrello_utente.istanze_biglietti.all()

        carrelli_totali = Carrello.objects.all()


        # Contolla che l'utente abbia fornito tutte le informazioni valide per il pagamento
        try:
            if not user.first_name:
                raise Exception('Nome non inserito')
            
            if not user.last_name:
                raise Exception('Cognome non inserito')
            
            if not utente.carta_credito:
                raise Exception('Numero carta non inserito')
            elif not re.match(r'^[0-9]{10,19}$', utente.carta_credito):
                raise Exception('Numero carta non valido')
            
            if not utente.scadenza_carta:
                raise Exception('Scadenza carta non inserita')
            elif utente.scadenza_carta < date.today():
                raise Exception('Carta scaduta')

            if not utente.cvv:
                raise Exception('CVV non inserito')
            elif not re.match(r'^[0-9]{3}$', utente.cvv):
                raise Exception('CVV non valido')
            
            if not carrello_utente.istanze_biglietti.all():
                raise Exception('Carrello vuoto')
        except Exception as e:
            return redirect(reverse('store:cart') + f'?error={e}')

        for biglietto in biglietti_carrello:
            prezzo_tassato = biglietto.tipologia_biglietto.prezzo + (biglietto.tipologia_biglietto.prezzo * CartView.IVA)
            ordine = Ordine.objects.create(data=date.today(), utente=utente, prezzo=prezzo_tassato)
            ordine.biglietto_digitale = generate_ticket(ordine.id, 
                                                        user.first_name, 
                                                        user.last_name, 
                                                        biglietto.tipologia_biglietto.gestore_circuito.gestione_circuito.nome, 
                                                        biglietto.tipologia_biglietto.settore, 
                                                        biglietto.tipologia_biglietto.data_evento, 
                                                        biglietto.numero_posto)
            ordine.save()

            biglietto.ordine = ordine
            biglietto.save()

            # Imposta il booleano delle notifiche a True per l'utente
            biglietto.tipologia_biglietto.gestore_circuito.notifiche = True
            Notifica.objects.create(descrizione=f'Ordine {ordine.pk} effettuato con successo', data=date.today(), ordine=ordine)

        # Imposta il booleano delle notifiche a True per l'Utente
        utente.notifiche = True
        utente.save()


        # Rimuove i biglietti comprati dal carrello di ogni utente
        for biglietto in biglietti_carrello:
            for carrello in carrelli_totali:
                carrello.istanze_biglietti.remove(biglietto)


        return redirect(reverse('store:cart') + '?purchase=ok')
    

class GestoreProfileDataChangeViewUpdate(LoginRequiredMixin, UpdateView):
    '''Classe che gestisce la modifica dei dati del gestore'''
    model = Gestore_Circuito
    template_name = 'store/gestore_profile_data_change.html'
    success_url = '/store/profile/'
    form_error_messages = ''

    user_data_form = GestoreProfileFormData()

    
    def get_form(self, form_class=None):

        gestore = Gestore_Circuito.objects.get(user=self.request.user)

        initial_data = {
            'indirizzo': gestore.indirizzo,
            'telefono': gestore.telefono,
            'email': gestore.user.email,
            'sito_web': gestore.sito_web,
            'iban': gestore.iban,
        }

        self.user_data_form = GestoreProfileFormData(initial=initial_data)        

        return self.user_data_form

    def get_object(self):
        return get_object_or_404(Gestore_Circuito, user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        # Recupera e aggiorna l'istanza gestore
        self.form_error_messages = ''
        gestore = Gestore_Circuito.objects.get(user=self.request.user)
        
        if self.are_inputs_correct():

            gestore.indirizzo = request.POST.get('indirizzo')
            gestore.telefono = request.POST.get('telefono')
            gestore.user.email = request.POST.get('email')
            gestore.sito_web = request.POST.get('sito_web')
            gestore.iban = request.POST.get('iban')
            
            
            gestore.save()
            gestore.user.save()

            messages.success(request, 'Dati del profilo salvati con successo')
            return redirect('store:profile')
        else:
            messages.error(request, self.form_error_messages)
            return redirect('store:profile')
    
    def are_inputs_correct(self):
        check_function_list = [
            self.check_address,
            self.check_phone,
            self.check_email,
            self.check_website,
            self.check_iban,
        ]
        for check_function in check_function_list:
            check_function()

        if self.form_error_messages == '':
            return True
        else:
            return False
              
    def check_address(self):
        if not re.match(r'[a-z,A-Z,0-9,àèéòùì\'/ ]+$', self.request.POST.get('indirizzo')):
            self.form_error_messages = f'{self.form_error_messages}- L\'indirizzo non può contenere caratteri speciali'

    def check_email(self):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', self.request.POST.get('email')):
            self.form_error_messages = f'{self.form_error_messages}- L\'email inserita non è valida'

    def check_phone(self):
        if not re.match(r'^\+?[0-9]{7,12}$', self.request.POST.get('telefono')):
            self.form_error_messages = f'{self.form_error_messages}- Il numero di telefono inserito non è valido'

    def check_iban(self):
        if not re.match(r'^[A-Z,a-z,0-9]{27}$', self.request.POST.get('iban')):
            if not self.request.POST.get('iban') == '':
                self.form_error_messages = f'{self.form_error_messages}- L\'IBAN inserito non è valido'

    def check_website(self):
        if not re.match(r'^www\.[A-Za-z0-9]+\.[a-z]{2,3}$', self.request.POST.get('sito_web')):
            if not self.request.POST.get('sito_web') == '':
                self.form_error_messages = f'{self.form_error_messages}- Il sito web inserito non è valido'


class CreateTicketTypeView(LoginRequiredMixin, CreateView):
    '''Classe per la creazione di una tipologia di biglietto'''
    model = TipologiaBiglietto
    template_name = 'store/create_ticket_type.html'
    success_url = '/store/profile/'
    form_error_messages = ''

    def get_form(self, form_class=None):
        return CreateTicketTypeForm()

    def post(self, request, *args, **kwargs):
        self.form_error_messages = ''
        gestore = Gestore_Circuito.objects.get(user=self.request.user)
        
        if self.are_inputs_correct():

            tipologia_biglietto = TipologiaBiglietto()
            tipologia_biglietto.settore = request.POST.get('settore')
            tipologia_biglietto.data_evento = request.POST.get('data_evento')
            tipologia_biglietto.prezzo = request.POST.get('prezzo')
            tipologia_biglietto.gestore_circuito = gestore

            tipologia_biglietto.save()

            messages.success(request, 'Tipologia biglietto creata con successo')
            return redirect('store:profile')
        else:
            messages.error(request, self.form_error_messages)
            return redirect('store:profile')
    
    def are_inputs_correct(self):
        check_function_list = [
            self.check_sector,
            self.check_date,
            self.check_price,
        ]
        for check_function in check_function_list:
            check_function()

        if self.form_error_messages == '':
            return True
        else:
            return False
              
    def check_sector(self):
        if not self.request.POST.get('settore').isalnum():
            self.form_error_messages = f'{self.form_error_messages}- Il settore non può contenere caratteri speciali'
        
        if not TipologiaBiglietto.objects.filter(settore=self.request.POST.get('settore')).count() == 0:
            self.form_error_messages = f'{self.form_error_messages}- Il settore inserito è già stato utilizzato'

    def check_date(self):
        if not date.fromisoformat(self.request.POST.get('data_evento')) > date.today():
            self.form_error_messages = f'{self.form_error_messages}- La data non può essere nel passato'

    def check_price(self):
        if not re.match(r'^[0-9]+\.?[0-9]*$', self.request.POST.get('prezzo')):
            self.form_error_messages = f'{self.form_error_messages}- Il prezzo inserito non è valido'


class CreateTicketInstanceView(LoginRequiredMixin, CreateView):
    '''Classe per la creazione dell'istanza di una tipologia di biglietto'''
    model = IstanzaBiglietto
    template_name = 'store/create_ticket_instance.html'
    success_url = '/store/profile/'
    form_error_messages = ''

    def get_form(self, form_class=None):
        gestore_circuito = Gestore_Circuito.objects.get(user=self.request.user)
        tipologia_biglietto = TipologiaBiglietto.objects.filter(gestore_circuito=gestore_circuito)

        self.ticket_data_form = CreateTicketInstanceForm()   
        choices = [(tipologia_biglietto.pk, f'{gestore_circuito.gestione_circuito.nome} - Settore {tipologia_biglietto.settore}') for tipologia_biglietto in tipologia_biglietto]
        self.ticket_data_form.fields['tipologia_biglietto'].choices = choices

        return self.ticket_data_form

    def post(self, request, *args, **kwargs):
        self.form_error_messages = ''
        gestore = Gestore_Circuito.objects.get(user=self.request.user)
        
        if self.are_inputs_correct():

            istanza_biglietto = IstanzaBiglietto()
            istanza_biglietto.numero_posto = request.POST.get('numero_posto')
            istanza_biglietto.tipologia_biglietto = TipologiaBiglietto.objects.get(pk=request.POST.get('tipologia_biglietto'))

            istanza_biglietto.save()

            messages.success(request, 'Istanza biglietto creata con successo')
            return redirect('store:profile')
        else:
            messages.error(request, self.form_error_messages)
            return redirect('store:profile')
    
    def are_inputs_correct(self):
        self.check_seat()

        if self.form_error_messages == '':
            return True
        else:
            return False
              
    def check_seat(self):
        if not re.match(r'^[0-9]+$', self.request.POST.get('numero_posto')):
            self.form_error_messages = f'{self.form_error_messages}- Il posto inserito non è valido. Può solo contentere numeri'

    
    
