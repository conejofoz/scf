from django.db import models

from bases.models import ClaseModelo

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
        return '{} {}'.format(self.nome, self.nome)

    def save(self):
        self.nome = self.nome.upper()
        self.sobrenome = self.sobrenome.upper()
        super(Cliente, self).save()

    class Meta:
        verbose_name_plural = 'Clientes'



    


    