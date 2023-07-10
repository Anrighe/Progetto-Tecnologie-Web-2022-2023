from django.db import models
from F1.validators import valida_non_negativi
from django_countries.fields import CountryField



class Scuderia(models.Model):
    nome = models.CharField(max_length=50)
    descrizione = models.CharField(max_length=10000)
    modello_vettura = models.CharField(max_length=50)
    modello_power_unit = models.CharField(max_length=50, default='')
    sede = models.CharField(max_length=100, default='')
    immagine_vettura = models.CharField(max_length=100)
    team_principal = models.CharField(max_length=100, default='')
    logo = models.CharField(max_length=100)
    punti = models.PositiveIntegerField(default=0)
    immagine1 = models.CharField(max_length=100, default='', blank=True)
    immagine2 = models.CharField(max_length=100, default='', blank=True)
    campionati_vinti = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Scuderie'


class Pilota(models.Model):
    nome = models.CharField(max_length=50)
    data = models.DateField()
    paese = CountryField(null=True, blank=True, default=None)
    foto_pilota = models.CharField(max_length=100, default='')
    foto_casco = models.CharField(max_length=100, default='')
    numero_gare = models.PositiveIntegerField(default=0)
    podi = models.PositiveIntegerField(default=0)
    campionati_vinti = models.PositiveIntegerField(default=0)
    biografia = models.CharField(max_length=10000, default='')
    immagine1 = models.CharField(max_length=100, default='', blank=True)
    immagine2 = models.CharField(max_length=100, default='', blank=True)

    # Un pilota è ingaggiato da una sola scuderia
    scuderia = models.ForeignKey(Scuderia, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Piloti'


class Circuito(models.Model):
    nome = models.CharField(max_length=50)
    paese = CountryField(null=True, blank=True, default=None)
    capienza_persone = models.PositiveIntegerField()
    lunghezza = models.FloatField(validators=[valida_non_negativi])
    preview = models.CharField(max_length=100)
    immagine_circuito = models.CharField(max_length=100)
    immagine_mappa = models.CharField(max_length=100)
    giro_veloce = models.CharField(max_length=100)
    numero_giri = models.PositiveIntegerField()
    inaugurazione = models.DateField()
    storia = models.CharField(max_length=10000, default='')

    class Meta:
        verbose_name_plural = 'Circuiti'


class Sessione(models.Model):
    tipo = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Sessioni'


class Partecipazione(models.Model):
    # null=True perché un pilota potrebbe non avere un tempo o partecipare a una determinata sessione
    miglior_tempo = models.CharField(max_length=100, null=True)  
    data = models.DateField(null=True)
    posizione = models.PositiveIntegerField(default=0)
    punti = models.PositiveIntegerField(default=0)

    # Una partecipazione si riferisce a una e una sola sessione
    sessione = models.ForeignKey(Sessione, on_delete=models.PROTECT, null=True, blank=True)

    # Una partecipazione si riferisce a uno e un solo circuito
    circuito = models.ForeignKey(Circuito, on_delete=models.PROTECT, null=True, blank=True)

    # Una partecipazione si riferisce a uno e un solo pilota
    pilota = models.ForeignKey(Pilota, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Partecipazioni'





















