from django.db import models

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
    

class FaturaDet(ClaseModelo2):
    fatura = models.ForeignKey(FaturaEnc, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.BigIntegerField(default=0)
    preco = models.FloatField(default=0)
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




