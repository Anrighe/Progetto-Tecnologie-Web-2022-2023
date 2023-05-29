from django.db import models
from F1.validators import valida_non_negativi


class Pilota(models.Model):
    nome = models.CharField(max_length=50)
    eta = models.PositiveSmallIntegerField()
    data = models.DateField()
    foto = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Piloti'


class Circuito(models.Model):
    nome = models.CharField(max_length=50)
    paese = models.CharField(max_length=50)
    capienza_persone = models.PositiveIntegerField()
    lunghezza = models.FloatField(validators=[valida_non_negativi])
    immagine = models.CharField(max_length=100)
    giro_veloce = models.DurationField()
    numero_giri = models.PositiveIntegerField()
    inaugurazione = models.DateField()

    class Meta:
        verbose_name_plural = 'Circuiti'


class Sessione(models.Model):
    tipo = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Sessioni'


class Partecipazione(models.Model):
    # null=True perché un pilota potrebbe non avere un tempo o partecipare a una determinata sessione
    miglior_tempo = models.DurationField(null=True)  
    data = models.DateField(null=True)

    class Meta:
        verbose_name_plural = 'Partecipazioni'


class Scuderia(models.Model):
    nome = models.CharField(max_length=50)
    descrizione = models.CharField(max_length=50)
    modello_vettura = models.CharField(max_length=50)
    immagine_vettura = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Scuderie'

# Una scuderia ingaggia da 0 a N piloti e un pilota è ingaggiato da una sola scuderia
Scuderia.ingaggia = models.ForeignKey(Pilota, on_delete=models.PROTECT, null=True, blank=True)

# In una sessione ci sono da 0 a N partecipazioni e una partecipazione si riferisce a una e una sola sessione
Sessione.vanta = models.ForeignKey(Partecipazione, on_delete=models.CASCADE, null=True, blank=True)

# In un circuito ci sono da 0 a N partecipazioni e una partecipazione si riferisce a uno e un solo circuito
Sessione.vanta = models.ForeignKey(Partecipazione, on_delete=models.CASCADE, null=True, blank=True)

# Un pilota effettua da 0 a N partecipazioni e una partecipazione si riferisce a uno e un solo pilota
Pilota.effettua = models.ForeignKey(Partecipazione, on_delete=models.CASCADE, null=True, blank=True)






