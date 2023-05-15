from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from F1.validators import valida_non_negativi, valida_iban, valida_carta_credito, valida_cvv


class Notifica(models.Model):
    descrizione = models.CharField(max_length=100)
    data = models.DateField()


class Ordine(models.Model):
    data = models.DateField()
    

class Gestore_Circuito(models.Model):
    nome = models.CharField(max_length=50)
    sito_web = models.CharField(max_length=50)
    indirizzo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=25)
    iban = models.CharField(max_length=34, validators=[valida_iban])


class Biglietto(models.Model):
    titolo = models.CharField(max_length=50)
    prezzo = models.FloatField(validators=[valida_non_negativi])
    numero_posto = models.PositiveSmallIntegerField()


class Carrello(models.Model):
    pass


class Utente(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    indirizzo = models.CharField(max_length=50)
    paese = models.CharField(max_length=50)
    telefono = models.CharField(max_length=25)
    e_mail = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=128)
    immagine_profilo = models.CharField(max_length=100)
    premium = models.DateField(null=True)
    carta_credito = models.CharField(max_length=20, validators=[valida_carta_credito], null=True)
    cvv = models.CharField(max_length=3, validators=[valida_cvv], null=True)
    scadenza_carta = models.DateField(null=True)

    def imposta_password(self, raw_password):
        self.password = make_password(raw_password)

    def controlla_password(self, raw_password):
        return check_password(raw_password, self.password)
