from django.db import models
from store.models import Utente, Gestore_Circuito


class PortaleF1(models.Model):
    
    class Meta:
        verbose_name_plural = 'PortaliF1'

class News(models.Model):
    titolo = models.CharField(max_length=100)
    data = models.DateField()
    contenuto = models.CharField(max_length=500)
    autore = models.CharField(max_length=50)
    tags = models.CharField(max_length=250)  # tag separati dal carattere ,

    class Meta:
        verbose_name_plural = 'News'


class Highlight(models.Model):
    titolo = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    visualizzazioni = models.PositiveIntegerField()
    
# Al portale di F1 appartengono da 0 a N utenti, e ogni utente appartiene al portale di F1
PortaleF1.appartiene_utente = models.ForeignKey(Utente, on_delete=models.PROTECT, null=True, blank=True)

# Al portale di F1 appartengono da 0 a N gestori di un circuito, e ogni gestore appartiene al portale di F1
PortaleF1.appartiene_gestore = models.ForeignKey(Gestore_Circuito, on_delete=models.PROTECT, null=True, blank=True)

# Il portale di F1 contiene da 0 a N highlight e un highlight è contenuto nel portale di F1
PortaleF1.contiene_highlight = models.ForeignKey(Highlight, on_delete=models.PROTECT, null=True, blank=True)

# Il portale di F1 contiene da 0 a N news e una news è contenuta nel portale di F1
PortaleF1.contiene_news = models.ForeignKey(News, on_delete=models.PROTECT, null=True, blank=True)


