from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def valida_non_negativi(valore):
    if valore <= 0:
        raise ValidationError('Il valore non può essere negativo')

class Pilota(models.Model):
    nome = models.CharField(max_length=50)
    eta = models.PositiveSmallIntegerField()
    data = models.DateField()
    foto = models.CharField(max_length=100)

class Circuito(models.Model):
    nome = models.CharField(max_length=50)
    paese = models.CharField(max_length=50)
    capienza_persone = models.PositiveSmallIntegerField()
    lunghezza = models.FloatField(validators=[valida_non_negativi])
    giro_veloce = models.DurationField()
    inaugurazione = models.DateField()

class Sessione(models.Model):
    tipo = models.CharField(max_length=50)

class Partecipazione(models.Model):
    # null=True perché un pilota potrebbe non avere un tempo o partecipare a una determinata sessione
    miglior_tempo = models.DurationField(null=True)  
    data = models.DateField(null=True)

class Scuderia(models.Model):
    nome = models.CharField(max_length=50)
    descrizione = models.CharField(max_length=50)
    modello_vettura = models.CharField(max_length=50)
    immagine_vettura = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)

Scuderia.ingaggia = models.ForeignKey(Pilota, blank=True, on_delete=models.PROTECT)
Pilota.ingaggia = models.OneToOneField(Scuderia, on_delete=models.PROTECT)

Pilota.partecipa = models.ManyToManyField(Partecipazione, blank=True)
Partecipazione.partecipa_pilota = models.OneToOneField(Pilota, on_delete=models.PROTECT)

Circuito.partecipa = models.ManyToManyField(Partecipazione, blank=True)
Partecipazione.partecipa_circuito = models.OneToOneField(Circuito, on_delete=models.PROTECT)

Sessione.partecipa = models.ManyToManyField(Partecipazione, blank=True)
Partecipazione.partecipa_sessione = models.OneToOneField(Sessione, on_delete=models.PROTECT)






