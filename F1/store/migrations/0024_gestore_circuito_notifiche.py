# Generated by Django 4.2.2 on 2023-08-10 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_remove_tipologiabiglietto_totale_posti'),
    ]

    operations = [
        migrations.AddField(
            model_name='gestore_circuito',
            name='notifiche',
            field=models.BooleanField(default=False),
        ),
    ]
