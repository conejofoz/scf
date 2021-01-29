from django.db import models
#para signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from bases.models import ClaseModelo
from inv.models import Produto

class Fornecedor(ClaseModelo):
    descricao=models.CharField(max_length=100, unique=True)
    endereco=models.CharField(max_length=250, null=True, blank=True)
    contato=models.CharField(max_length=100)
    telefone=models.CharField(max_length=10, null=True, blank=True)
    email=models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.descricao)

    def save(self):
        self.descricao = self.descricao.upper()
        super(Fornecedor, self).save()

    class Meta:
        verbose_name_plural = 'Fornecedores'   


class ComprasEnc(ClaseModelo):
    data_compra=models.DateField(null=True, blank=True) 
    observacao=models.TextField(blank=True, null=True)
    no_fatura=models.CharField(max_length=100)
    data_fatura=models.DateField()
    sub_total=models.FloatField(default=0)
    desconto=models.FloatField(default=0)
    total=models.FloatField(default=0)

    fornecedor=models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.observacao)

    def save(self):
        self.observacao = self.observacao.upper()
        self.total = self.sub_total - self.desconto
        super(ComprasEnc, self).save()
    
    class Meta:
        verbose_name_plural="Cabeçalho Compras"
        verbose_name='Cabeçalho Compra'


class ComprasDet(ClaseModelo):
    compra=models.ForeignKey(ComprasEnc, on_delete=models.CASCADE)
    produto=models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade=models.BigIntegerField(default=0)
    preco_forn=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    desconto=models.FloatField(default=0)
    total=models.FloatField(default=0)
    custo=models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.produto)

    def save(self):
        self.sub_total = float(float(int(self.quantidade)) * float(self.preco_forn))
        self.total = self.sub_total - float(self.desconto)
        super(ComprasDet, self).save()

    class Meta:
        verbose_name_plural="Detalhes Compras"
        verbose_name="Detalhe Compra"

    
@receiver(post_delete, sender=ComprasDet)
def detalhe_compra_delete(sender, instance, **kwargs):
    id_produto = instance.produto.id
    id_compra = instance.compra.id

    enc = ComprasEnc.objects.filter(pk=id_compra).first()
    if enc:
        sub_total=ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        desconto=ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('desconto'))
        enc.sub_total = sub_total["sub_total__sum"]
        enc.desconto = desconto["desconto__sum"]
        enc.save()

        prod = Produto.objects.filter(pk=id_produto).first()
        if prod:
            quantidade = int(prod.existencia) - int(instance.quantidade)
            prod.existencia = quantidade
            prod.save()

    
@receiver(post_save, sender=ComprasDet)
def detalhe_compra_salvar(sender, instance, **kwargs):
    id_produto = instance.produto.id
    data_compra = instance.compra.data_compra

    prod = Produto.objects.filter(pk=id_produto).first()
    if prod:
        quantidade = int(prod.existencia) + int(instance.quantidade)
        prod.existencia = quantidade
        prod.ultima_compra=data_compra
        prod.save()
    
