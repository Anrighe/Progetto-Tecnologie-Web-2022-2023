from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class FormUtente(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('Login', 'Login'))

    nome = forms.CharField(label='nome')
    e_mail = forms.EmailField(label='e_mail')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))