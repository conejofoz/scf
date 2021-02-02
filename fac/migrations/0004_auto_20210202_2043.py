# Generated by Django 3.1.5 on 2021-02-02 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0003_faturadet_sub_total'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faturadet',
            options={'permissions': [('sup_caixa_faturadet', 'Permissão de Supervisor de Caixa Detalhe')], 'verbose_name': 'Detalhe Fatura', 'verbose_name_plural': 'Detalhes Faturas'},
        ),
        migrations.AlterModelOptions(
            name='faturaenc',
            options={'permissions': [('sup_caixa_faturaenc', 'Permissão de Supervisor de Caixa Cabeçalho')], 'verbose_name': 'Cabeçalho fatura', 'verbose_name_plural': 'Cabeçalho faturas'},
        ),
    ]
