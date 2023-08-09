from django import forms
from django_countries import countries

class UtenteProfileFormData(forms.Form):
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
        super(UtenteProfileFormData, self).__init__(*args, **kwargs)
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


class GestoreProfileFormData(forms.Form):
    indirizzo = forms.CharField(label='Indirizzo', required=False, max_length=50)
    telefono = forms.CharField(label='Telefono', required=False, max_length=25, help_text='Formati telefonici validi (0-9): +391234567890, 1234567890')
    sito_web = forms.CharField(label='Sito web', required=False, max_length=100, help_text='Formato valido sito web: www.example.com')
    iban = forms.CharField(label='IBAN', required=False, max_length=27, help_text='Formato valido IBAN (0-9): IT00A1234567890123456789012')
    email = forms.EmailField(label='Email', required=False, max_length=100, help_text='Formato valido email: user_name@domain_name.tld')

    def __init__(self, *args, **kwargs):
        super(GestoreProfileFormData, self).__init__(*args, **kwargs)
        self.add_tooltips()
    
    def add_tooltips(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['title'] = field.label


class CreateTicketTypeForm(forms.Form):
    settore = forms.CharField(label='Settore', required=True, max_length=100, help_text='Caratteri validi per il settore (0-9)')
    data_evento = forms.DateField(label='Data evento', required=True, widget=forms.DateInput(attrs={'type': 'date'}), help_text='La data dell\'evento non può essere nel passato')
    prezzo = forms.FloatField(label='Prezzo', required=True, help_text='Il prezzo non può essere negativo')

    def __init__(self, *args, **kwargs):
        super(CreateTicketTypeForm, self).__init__(*args, **kwargs)
        self.add_tooltips()

    def add_tooltips(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['title'] = field.label


class CreateTicketInstanceForm(forms.Form):
    tipologia_biglietto = forms.ChoiceField(label='Tipologia biglietto', choices=[], required=True, initial="1")
    numero_posto = forms.IntegerField(label='Numero posto', required=True, help_text='Il numero del posto non può essere negativo')