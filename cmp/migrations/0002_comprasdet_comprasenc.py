# Generated by Django 3.1.5 on 2021-01-26 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0005_produto'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cmp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComprasEnc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('data_compra', models.DateField(blank=True, null=True)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('no_fatura', models.CharField(max_length=100)),
                ('data_fatura', models.DateField()),
                ('sub_total', models.FloatField(default=0)),
                ('desconto', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmp.fornecedor')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cabeçalho Compra',
                'verbose_name_plural': 'Cabeçalho Compras',
            },
        ),
        migrations.CreateModel(
            name='ComprasDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('quantidade', models.BigIntegerField(default=0)),
                ('preco_forn', models.FloatField(default=0)),
                ('sub_total', models.FloatField(default=0)),
                ('desconto', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('custo', models.FloatField(default=0)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmp.comprasenc')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.produto')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalhe Compra',
                'verbose_name_plural': 'Detalhes Compras',
            },
        ),
    ]
