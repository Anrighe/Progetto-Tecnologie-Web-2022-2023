# Generated by Django 4.2.1 on 2023-05-24 09:58

import F1.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circuito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('paese', models.CharField(max_length=50)),
                ('capienza_persone', models.PositiveIntegerField()),
                ('lunghezza', models.FloatField(validators=[F1.validators.valida_non_negativi])),
                ('giro_veloce', models.DurationField()),
                ('inaugurazione', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Circuiti',
            },
        ),
        migrations.CreateModel(
            name='Partecipazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miglior_tempo', models.DurationField(null=True)),
                ('data', models.DateField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Partecipazioni',
            },
        ),
        migrations.CreateModel(
            name='Pilota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('eta', models.PositiveSmallIntegerField()),
                ('data', models.DateField()),
                ('foto', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Piloti',
            },
        ),
        migrations.CreateModel(
            name='Scuderia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('descrizione', models.CharField(max_length=50)),
                ('modello_vettura', models.CharField(max_length=50)),
                ('immagine_vettura', models.CharField(max_length=100)),
                ('logo', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Scuderie',
            },
        ),
        migrations.CreateModel(
            name='Sessione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Sessioni',
            },
        ),
    ]
