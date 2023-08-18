from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Utente
from django.test.client import Client
from store.views import UtenteProfileDataChangeViewUpdate


class UtenteProfileDataChangeTestCase(TestCase):
    '''Testa la funzionalità di modifica dei dati del profilo di un utente'''

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.save()
        self.utente = Utente.objects.create(user=self.user)
        self.utente.save()

        self.client = Client()
        self.client.login(username='testuser', password='12345')

        self.profile_data_change = UtenteProfileDataChangeViewUpdate()      

    def test_utente_data_form_found(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.get(self.reverse_profile_data_change)
        self.assertEqual(self.response.status_code, 200)

    def test_utente_data_change_request_valid(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John',
            'cognome': 'Rossi', 
            'email': 'email@email.com', 
            'data_nascita': '2020-09-09', 
            'telefono': 3333333333, 
            'carta_credito': 12345678912345, 
            'cvv': 123, 'scadenza_carta': 
            '2029-09-09'
            }, follow=True)
        self.assertContains(self.response, 'Dati del profilo salvati con successo')

    def test_utente_data_change_request_invalid_nome(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': '#"£$%&/()=?^', # nome non valido
            'cognome': 'Rossi', 
            'email': 'email@email.com', 
            'data_nascita': '2020-09-09', 
            'telefono': 3333333333, 
            'carta_credito': 12345678912345, 
            'cvv': 123, 'scadenza_carta': 
            '2029-09-09'
            }, follow=True)
        self.assertContains(self.response, 'Il nome non può contenere numeri o caratteri speciali')

    def test_utente_data_change_request_invalid_cognome(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John', 
            'cognome': '#"£$%&/()=?^', # cognome non valido
            'email': 'email@email.com', 
            'data_nascita': '2020-09-09', 
            'telefono': 3333333333, 
            'carta_credito': 12345678912345, 
            'cvv': 123, 'scadenza_carta': 
            '2029-09-09'
            }, follow=True)
        self.assertContains(self.response, 'Il cognome non può contenere numeri o caratteri speciali')

    def test_utente_data_change_request_invalid_email(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John', 
            'cognome': 'Rossi', 
            'email': '4m0ng@em@il.5u5', # email non valida
            'data_nascita': '2020-09-09', 
            'telefono': 3333333333, 
            'carta_credito': 12345678912345, 
            'cvv': 123, 'scadenza_carta': 
            '2029-09-09'
            }, follow=True)
        self.assertContains(self.response, 'email inserita non è valida')

    def test_utente_data_change_request_invalid_future_birth_date(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John', 
            'cognome': 'Rossi', 
            'email': 'email@email.com',
            'data_nascita': '2199-09-09', # Data futura non valida
            'telefono': 3333333333, 
            'carta_credito': 12345678912345, 
            'cvv': 123, 'scadenza_carta': 
            '2029-09-09' 
            }, follow=True)
        self.assertContains(self.response, 'La data di nascita non può essere nel futuro')
        
    def test_utente_data_change_request_invalid_birth_date(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John', 
            'cognome': 'Rossi', 
            'email': 'email@email.com', 
            'data_nascita': '21adsa99-0//*9-09999', # Formato data non valido
            'telefono': 3333333333, 
            'carta_credito': 12345678912345, 
            'cvv': 123, 'scadenza_carta': 
            '2029-09-09' 
            }, follow=True)
        self.assertContains(self.response, 'La data di nascita inserita non è valida')

    def test_utente_data_change_request_invalid_phone_number(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John', 
            'cognome': 'Rossi', 
            'email': 'email@email.com', 
            'data_nascita': '2199-09-09', 
            'telefono': '++398860000000', # Formato numero di telefono non valido
            'carta_credito': 12345678912345, 
            'cvv': 123, 'scadenza_carta': 
            '2029-09-09' 
            }, follow=True)
        self.assertContains(self.response, 'Il numero di telefono inserito non è valido')        

    def test_utente_data_change_request_invalid_credit_card_number(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John', 
            'cognome': 'Rossi', 
            'email': 'email@email.com', 
            'data_nascita': '2199-09-09', 
            'telefono': 3333333333, 
            'carta_credito': 5559875412345678912345, # Carta di credito non valida
            'cvv': 123, 'scadenza_carta': 
            '2029-09-09' 
            }, follow=True)
        self.assertContains(self.response, 'Il numero di carta di credito inserito non è valido')                

    def test_utente_data_change_request_invalid_credit_card_expired(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John', 
            'cognome': 'Rossi', 
            'email': 'email@email.com', 
            'data_nascita': '2199-09-09', 
            'telefono': 3333333333, 
            'carta_credito': 12345678912345, 
            'cvv': 123, 
            'scadenza_carta': '2012-09-09' # Carta Scaduta
            }, follow=True)
        self.assertContains(self.response, 'La carta è scaduta')       

    def test_utente_data_change_request_invalid_credit_card_expiration_date(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John', 
            'cognome': 'Rossi', 
            'email': 'email@email.com', 
            'data_nascita': '2199-09-09', 
            'telefono': 3333333333, 
            'carta_credito': 12345678912345, 
            'cvv': 123, 
            'scadenza_carta': '2011232-0%%-09' # Formato data non valido
            }, follow=True)
        self.assertContains(self.response, 'La data inserita di scadenza della carta non è valida')      


    def test_utente_data_change_request_invalid_cvv(self):
        self.reverse_profile_data_change = reverse('store:modify_utente_update', kwargs={'pk': self.user.id})
        self.response = self.client.post(self.reverse_profile_data_change, {
            'nome': 'John', 
            'cognome': 'Rossi', 
            'email': 'email@email.com', 
            'data_nascita': '2199-09-09', 
            'telefono': 3333333333, 
            'carta_credito': 12345678912345, 
            'cvv': 123456, # CVV non valido
            'scadenza_carta': '2012-09-09' 
            }, follow=True)
        self.assertContains(self.response, 'Il CVV non è valido')     

    def tearDown(self):
        self.user.delete()
        self.utente.delete()
        