from django.db import models

from bases.models import ClaseModelo

class Categoria(ClaseModelo):
    descricao = models.CharField(max_length=100, help_text='Descrição da categoria', unique=True)

    def __str__(self):
        return '{}'.format(self.descricao)

    def save(self):
        self.descricao = self.descricao.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural = 'Categorias'
