from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from store.models import Utente
from django.core.files.storage import FileSystemStorage
import os
from PIL import Image
from django.contrib import messages
from django import forms
from django_countries.fields import CountryField
from django_countries import countries



class UserProfileFormData(forms.Form):
    nome = forms.CharField(label='Nome', required=False)
    cognome = forms.CharField(label='Cognome', required=False)
    email = forms.CharField(label='Email', required=False)
    indirizzo = forms.CharField(label='Indirizzo', required=False)
    data_nascita = forms.DateField(label='Data di nascita', required=False)
    sesso_choices = [('M', 'Maschio'), ('F', 'Femmina')]
    sesso = forms.ChoiceField(label='Sesso', choices=sesso_choices, required=False, initial="F")
    paese = forms.ChoiceField(label='Paese', choices=countries, required=False, initial='IT')
    telefono = forms.CharField(label='Telefono', required=False)
    carta_credito = forms.CharField(label='Carta di credito', required=False)
    cvv = forms.CharField(label='CVV', required=False)
    scadenza_carta = forms.DateField(label='Scadenza carta', required=False)


# Classe che gestisce la modifica dei dati dell'utente
class UserProfileDataChangeView(LoginRequiredMixin, ListView):
    model = Utente
    form_class = UserProfileFormData
    template_name = 'store/user_profile_data_change.html'
    success_url = 'modify'  # Specify the URL to redirect to after successful form submission

    user_data_form = UserProfileFormData()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

        #print("paese:", user[0].paese.name)
        #user_country = user[0].paese  # Assuming the user's country is stored in the profile model
        #if user_country:
            #initial_data['paese'] = user_country.name

        context['form'] = self.form_class(initial=initial_data)
        return context




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