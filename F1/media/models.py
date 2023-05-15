from django.db import models


class PortaleF1(models.Model):
    titolo = models.CharField(max_length=100)


class News(models.Model):
    titolo = models.CharField(max_length=100)
    data = models.DateField()
    contenuto = models.CharField(max_length=500)
    autore = models.CharField(max_length=50)
    tags = models.CharField(max_length=250)  # tag separati dal carattere ,

class Highlight(models.Model):
    titolo = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    visualizzazioni = models.PositiveIntegerField()
    

News.contiene = models.OneToOneField(PortaleF1, on_delete=models.PROTECT)
PortaleF1.contiene_news = models.ManyToManyField(News, blank=True)
Highlight.contiene = models.OneToOneField(PortaleF1, on_delete=models.PROTECT)
PortaleF1.contiene_highlight = models.ManyToManyField(Highlight, blank=True)


