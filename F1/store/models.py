from django.db import models
from F1.validators import valida_non_negativi, valida_iban, valida_carta_credito, valida_cvv
from django.contrib.auth.models import User
from info.models import Circuito


class Gestore_Circuito(models.Model):
    sito_web = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=25)
    iban = models.CharField(max_length=34, validators=[valida_iban])

    # Un gestore di un circuito gestisce uno e un solo circuito e un circuito è gestito da uno e un solo gestore
    gestione_circuito = models.OneToOneField(Circuito, on_delete=models.PROTECT, null=True, blank=True)

    # Connette i gestori dei circuiti con la table User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Gestori circuiti'


class Utente(models.Model):
    indirizzo = models.CharField(max_length=50)
    paese = models.CharField(max_length=50)
    telefono = models.CharField(max_length=25)
    immagine_profilo = models.CharField(max_length=100)
    premium = models.DateField(null=True, blank=True)
    carta_credito = models.CharField(max_length=19, validators=[valida_carta_credito], null=True)
    cvv = models.CharField(max_length=3, validators=[valida_cvv], null=True)
    scadenza_carta = models.DateField(null=True)
    notifiche = models.BooleanField(null=False, default=False)

    # Connette gli utenti con la table User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Utenti'


class Ordine(models.Model):
    data = models.DateField()
    
    # Un ordine si riferisce a uno e un solo gestore di un circuito
    gestore_circuito = models.ForeignKey(Gestore_Circuito, on_delete=models.PROTECT, null=False, blank=False)

    # Un ordine si riferisce a uno e un solo utente
    utente = models.ForeignKey(Utente, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Ordini'   


class Notifica(models.Model):
    descrizione = models.CharField(max_length=100)
    data = models.DateField()

    # Una notifica si riferisce al più a un ordine
    ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Notifiche'


class Carrello(models.Model):
    # Un preciso carrello è posseduto da uno e un solo utente
    # In caso di cancellazione dell'utente è necessario cancellare anche il carrello
    possedimento_carrello = models.OneToOneField(Utente, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = 'Carrelli'


class Biglietto(models.Model):
    titolo = models.CharField(max_length=50)
    prezzo = models.FloatField(validators=[valida_non_negativi])
    numero_posto = models.PositiveIntegerField()

    # Se un preciso biglietto è stato acquistato è contenuto in al più un ordine
    # Se non è stato acquistato non è contenuto in nessun ordine
    ordine = models.ForeignKey(Ordine, on_delete=models.PROTECT, null=True, blank=True)

    # Un preciso biglietto può essere contenuto da 0 a N carrelli
    # Esempio: più utenti hanno inserito lo stesso biglietto nel proprio carrello
    carrello = models.ManyToManyField(Carrello, blank=True)

    # Un preciso biglietto viene pubblicato nel negozio da uno e un solo gestore di un circuito
    gestore_circuito = models.ForeignKey(Gestore_Circuito, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Bliglietti'











