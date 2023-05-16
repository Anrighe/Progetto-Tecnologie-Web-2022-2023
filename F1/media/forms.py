from django import forms

class FormUtente(forms.Form):
    nome = forms.CharField(label='nome')
    e_mail = forms.EmailField(label='e_mail')
