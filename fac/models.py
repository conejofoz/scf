from django.db import models

#para signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum


from bases.models import ClaseModelo, ClaseModelo2
from inv.models import Produto

class Cliente(ClaseModelo):
    NAT='Natural'
    JUR='Jurídica'
    TIPO_CLIENTE = [
        (NAT, 'Natural'),
        (JUR, 'Jurídica'),
    ]
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    celular = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CLIENTE, default=NAT)

    def __str__(self):
        return '{} {}'.format(self.nome, self.sobrenome)

    def save(self):
        self.nome = self.nome.upper()
        self.sobrenome = self.sobrenome.upper()
        super(Cliente, self).save()

    class Meta:
        verbose_name_plural = 'Clientes'


class FaturaEnc(ClaseModelo2):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    sub_total=models.FloatField(default=0)
    desconto=models.FloatField(default=0)
    total=models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        self.total = self.sub_total - self.desconto
        super(FaturaEnc, self).save()

    class Meta:
        verbose_name_plural = 'Cabeçalho faturas'
        verbose_name = 'Cabeçalho fatura'
        permissions = [
            ('sup_caixa_faturaenc', 'Permissão de Supervisor de Caixa Cabeçalho')
        ]
    

class FaturaDet(ClaseModelo2):
    fatura = models.ForeignKey(FaturaEnc, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.BigIntegerField(default=0)
    preco = models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    desconto = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.produto)

    def save(self):
        self.sub_total = float(float(int(self.quantidade)) * float(self.preco))    
        self.total = self.sub_total - float(self.desconto)
        super(FaturaDet, self).save()

    class Meta:
        verbose_name_plural="Detalhes Faturas"
        verbose_name='Detalhe Fatura'
        permissions = [
            ('sup_caixa_faturadet', 'Permissão de Supervisor de Caixa Detalhe')
        ]


@receiver(post_save, sender=FaturaDet)
def detalhe_fac_salvar(sender, instance, **kwargs):
    #ATUALIZAR OS TOTAIS NO CABEÇALHO DA FATURA
    fatura_id = instance.fatura.id
    produto_id = instance.produto.id

    enc = FaturaEnc.objects.get(pk=fatura_id)
    if enc:
        sub_total=FaturaDet.objects.filter(fatura=fatura_id).aggregate(sub_total=Sum('sub_total')).get('sub_total',0.00)
        #sub_total=ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        
        desconto = FaturaDet.objects.filter(fatura=fatura_id).aggregate(desconto=Sum('desconto')).get('desconto',0.00)

    enc.sub_total = sub_total
    enc.desconto = desconto
    enc.save()


    #ATUALIZAR O ESTOQUE
    prod=Produto.objects.filter(pk=produto_id).first()
    if prod:
        quantidade = int(prod.existencia) - int(instance.quantidade)
        prod.existencia = quantidade
        prod.save()
    


