from django import forms
from django_countries import countries

class UserProfileFormData(forms.Form):
    nome = forms.CharField(label='Nome', required=False, max_length=100, help_text='Caratteri validi per il nome (a-z, A-Z)')
    cognome = forms.CharField(label='Cognome', required=False, max_length=100, help_text='Caratteri validi per il cognome (a-z, A-Z)')
    email = forms.CharField(label='Email', required=False, max_length=100, help_text='Formato valido email: user_name@domain_name.tld')
    indirizzo = forms.CharField(label='Indirizzo', required=False, max_length=50)
    data_nascita = forms.DateField(label='Data di nascita', required=False, widget=forms.DateInput(attrs={'type': 'date'}), help_text='La data di nascita non può essere nel futuro')
    sesso_choices = [('M', 'Maschio'), ('F', 'Femmina')]
    sesso = forms.ChoiceField(label='Sesso', choices=sesso_choices, required=False, initial="F")
    paese = forms.ChoiceField(label='Paese', choices=countries, required=False, initial='IT')
    telefono = forms.CharField(label='Telefono', required=False, max_length=25, help_text='Formati telefonici validi (0-9): +391234567890, 1234567890')
    carta_credito = forms.CharField(label='Carta di credito', required=False, max_length=19, help_text='Formato valido carta di credito (0-9): 1234123412341234')
    cvv = forms.CharField(label='CVV', required=False, max_length=3, help_text='Formato valido CVV (0-9): 123')
    scadenza_carta = forms.DateField(label='Scadenza carta', required=False, widget=forms.DateInput(attrs={'type': 'date'}), help_text='La data di scadenza non può essere nel passato')
    
    def __init__(self, *args, **kwargs):
        super(UserProfileFormData, self).__init__(*args, **kwargs)
        self.add_tooltips()

    def add_tooltips(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['title'] = field.label
        

class TicketForm(forms.Form):
    
    istanze_biglietti = forms.ChoiceField(label='', choices=[], required=True, initial="1")
    
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.add_tooltips()

    def add_tooltips(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['title'] = field.label