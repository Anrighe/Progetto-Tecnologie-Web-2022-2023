from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from F1.validators import valida_non_negativi, valida_iban, valida_carta_credito, valida_cvv
from media.models import PortaleF1
from info.models import Circuito


class Notifica(models.Model):
    descrizione = models.CharField(max_length=100)
    data = models.DateField()


class Ordine(models.Model):
    data = models.DateField()
    

class Gestore_Circuito(models.Model):
    nome = models.CharField(max_length=50)
    sito_web = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=25)
    iban = models.CharField(max_length=34, validators=[valida_iban])
    e_mail = models.CharField(max_length=25, unique=True)


class Biglietto(models.Model):
    titolo = models.CharField(max_length=50)
    prezzo = models.FloatField(validators=[valida_non_negativi])
    numero_posto = models.PositiveIntegerField()


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
    carta_credito = models.CharField(max_length=19, validators=[valida_carta_credito], null=True)
    cvv = models.CharField(max_length=3, validators=[valida_cvv], null=True)
    scadenza_carta = models.DateField(null=True)

    def imposta_password(self, raw_password):
        self.password = make_password(raw_password)

    def controlla_password(self, raw_password):
        return check_password(raw_password, self.password)

# Una notifica è generata al più da un ordine 
# Se viene cancellato l'ordine, viene cancellata la notifica
Notifica.genera = models.OneToOneField(Ordine, on_delete=models.CASCADE, null=True, blank=True)  

# Un ordine genera da 0 a N notifiche
Ordine.genera = models.ManyToManyField(Notifica, null=True, blank=True)

# Dato un preciso ordine, esso è ricevuto da uno e un solo gestore di un circuito
# Se viene cancellato un gestore di un circuito, gli ordini ad esso associato non vengono cancellati
Ordine.riceve = models.OneToOneField(Gestore_Circuito, on_delete=models.PROTECT)

# Un gestore di un circuito riceve da 0 a N ordini
Gestore_Circuito.riceve = models.ManyToManyField(Ordine, null=True, blank=True)

# Un gestore di un circuito appartiene a uno e un solo portale di F1
Gestore_Circuito.appartiene = models.OneToOneField(PortaleF1)

# Un gestore di un circuito gestisce uno e un solo circuito
# Se viene cancellato un circuito, il gestore di un circuito non dev'essere cancellato
Gestore_Circuito.gestisce = models.OneToOneField(Circuito, on_delete=models.PROTECT, null=True)

# Un ordine contiene da 1 a N biglietti
Ordine.contiene = models.ManyToManyField(Biglietto)

# Se un preciso biglietto è stato acquistato è contenuto in al più un ordine
# Se non è stato acquistato non è contenuto in nessun ordine
# Se l'ordine viene cancellato, il biglietto non dev'essere cancellato
Biglietto.contiene_ordine = models.OneToOneField(Ordine, on_delete=models.PROTECT, null=True, blank=True)

# Un preciso biglietto può essere contenuto da 0 a N carrelli
# Esempio: più utenti hanno inserito lo stesso biglietto nel proprio carrello
Biglietto.contiene_carrello = models.ManyToManyField(Carrello, null=True, blank=True)

# Un carrello può contenere da 0 a N biglietti
Carrello.contiene = models.ManyToManyField(Biglietto, null=True, blank=True)

# Un preciso carrello è posseduto da uno e un solo utente
# In caso di cancellazione dell'utente è necessario cancellare anche il carrello
Carrello.possiede = models.OneToOneField(Utente, on_delete=models.CASCADE)

# Un utente possiede uno e un solo carrello
Utente.possiede = models.OneToOneField(Utente)

# Un utente fa parte di uno e un solo portale di F1
Utente.appartiene = models.OneToOneField(PortaleF1)



