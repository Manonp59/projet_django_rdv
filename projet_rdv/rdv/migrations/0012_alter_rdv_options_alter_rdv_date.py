# Generated by Django 4.1.5 on 2023-02-13 09:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdv', '0011_alter_rdv_options_alter_rdv_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rdv',
            options={'permissions': (('creer_creneau', 'creer un nouveau creneau'), ('supprimer_creneau', 'supprimer un creneau'), ('ajouter_note', 'ajouter une note'), ('modifier_note', 'modifier la note'))},
        ),
        migrations.AlterField(
            model_name='rdv',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 9, 27, 31, 740083, tzinfo=datetime.timezone.utc)),
        ),
    ]