from django import forms
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