from django.db import models
from info.models import Scuderia

class PortaleF1(models.Model):
    
    class Meta:
        verbose_name_plural = 'PortaliF1'

class News(models.Model):
    titolo = models.CharField(max_length=100)
    data = models.DateField()
    tags = models.ManyToManyField(Scuderia, blank=True, default=None)
    link_news = models.CharField(max_length=250, default='')
    immagine = models.CharField(max_length=250, default='')

    
    # Il portale di F1 contiene da 0 a N news e una news è contenuta nel portale di F1
    portale_f1 = models.ForeignKey(PortaleF1, on_delete=models.PROTECT, null=True, blank=True)

    #def __str__(self):
        #return f'{self.titolo} - {self.contenuto} - {self.data}'

    class Meta:
        verbose_name_plural = 'News'


class Highlight(models.Model):
    titolo = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    data = models.DateField()
    visualizzazioni = models.PositiveIntegerField(default=0)
    preview = models.CharField(max_length=200)

    # Il portale di F1 contiene da 0 a N highlight e un highlight è contenuto nel portale di F1
    portale_f1 = models.ForeignKey(PortaleF1, on_delete=models.PROTECT, null=True, blank=True)
    
    








