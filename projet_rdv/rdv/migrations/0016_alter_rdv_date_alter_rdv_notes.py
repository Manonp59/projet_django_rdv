# Generated by Django 4.1.5 on 2023-02-14 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdv', '0015_alter_rdv_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rdv',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 14, 15, 12, 50, 169316, tzinfo=datetime.timezone.utc), unique=True),
        ),
        migrations.AlterField(
            model_name='rdv',
            name='notes',
            field=models.CharField(max_length=1000),
        ),
    ]