# Generated by Django 3.1.5 on 2021-02-02 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0002_faturadet_faturaenc'),
    ]

    operations = [
        migrations.AddField(
            model_name='faturadet',
            name='sub_total',
            field=models.FloatField(default=0),
        ),
    ]
