from django.db import models
from F1.validators import valida_non_negativi


class Scuderia(models.Model):
    nome = models.CharField(max_length=50)
    descrizione = models.CharField(max_length=50)
    modello_vettura = models.CharField(max_length=50)
    immagine_vettura = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)
    punti = models.PositiveIntegerField(default=0)
    immagine1 = models.CharField(max_length=100, default='')
    immagine2 = models.CharField(max_length=100, default='')

    class Meta:
        verbose_name_plural = 'Scuderie'


class Pilota(models.Model):
    nome = models.CharField(max_length=50)
    eta = models.PositiveSmallIntegerField()
    data = models.DateField()
    foto = models.CharField(max_length=100)

    # Un pilota è ingaggiato da una sola scuderia
    scuderia = models.ForeignKey(Scuderia, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Piloti'


class Circuito(models.Model):
    nome = models.CharField(max_length=50)
    paese = models.CharField(max_length=50)
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

    # Una partecipazione si riferisce a una e una sola sessione
    sessione = models.ForeignKey(Sessione, on_delete=models.PROTECT, null=True, blank=True)

    # Una partecipazione si riferisce a uno e un solo circuito
    circuito = models.ForeignKey(Circuito, on_delete=models.PROTECT, null=True, blank=True)

    # Una partecipazione si riferisce a uno e un solo pilota
    pilota = models.ForeignKey(Pilota, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Partecipazioni'





















