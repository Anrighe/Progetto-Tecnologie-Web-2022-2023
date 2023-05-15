from django.contrib.postgres.fields import ArrayField
from django.db import models


class News(models.Model):
    titolo = models.CharField(max_length=100)
    data = models.DateField()
    contenuto = models.CharField(max_length=500)
    autore = models.CharField(max_length=50)
    #tag = ArrayField(models.CharField(max_length=25), size=10,)