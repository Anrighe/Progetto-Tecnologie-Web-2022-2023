from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from store.models import Utente
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
from store.forms import UserProfileFormData





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
                    print("FILENAME", filename)

                    utente.immagine_profilo = f'/static/users/{username}/{filename}'
                    utente.save()
                else:
                    messages.error(request, 'Formato dell\'immagine non valido. Utilizza un file in formato JPEG, JPG, o PNG.')
            else:
                messages.error(request, 'Non è stata caricata nessuna immagine.')

    except Utente.DoesNotExist:
        utente = None

    ctx = {'utente': utente}

    return render(request, 'store/user_profile.html', ctx)    