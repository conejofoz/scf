from django.db import models

from bases.models import ClaseModelo

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
    
    
