# Generated by Django 4.2.4 on 2023-08-19 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0011_circuito_data_evento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pilota',
            old_name='immagine1',
            new_name='immagine',
        ),
    ]
