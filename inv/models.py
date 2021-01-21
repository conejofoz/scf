from django.db import models

from bases.models import ClaseModelo

class Categoria(ClaseModelo):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.descricao)

    def save(self):
        self.descricao = self.descricao.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural = 'Categorias'


class SubCategoria(ClaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=100)
    #não podemos usar unique porque pode ser que tenho uma subcategoria com o mesmo nome
    #mais em outra categoria

    def __str__(self):
        return '{}:{}'.format(self.categoria.descricao, self.descricao)

    def save(self):
        self.descricao = self.descricao.upper()
        super(SubCategoria, self).save()

    class Meta:
        verbose_name_plural='Sub Categorias'
        unique_together = ('categoria', 'descricao')
        #unique composto.. só pode haver uma categoria com a mesma descricao na subcategoria
        #uma vez que a categoria seja outra pode haver a mesma descricao novamente


class Marca(ClaseModelo):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.descricao)

    def save(self):
        self.descricao = self.descricao.upper()
        super(Marca, self).save()

    class Meta:
        verbose_name_plural = 'Marcas'


class UnidadeMedida(ClaseModelo):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.descricao)

    def save(self):
        self.descricao = self.descricao.upper()
        super(UnidadeMedida, self).save()

    class Meta:
        verbose_name_plural = 'Unidades de Medida'


class Produto(ClaseModelo):
    codigo=models.CharField(max_length=20, unique=True)        
    codigo_barra=models.CharField(max_length=50)
    descricao=models.CharField(max_length=200)
    preco=models.FloatField(default=0)
    existencia=models.IntegerField(default=0)
    ultima_compra=models.DateField(null=True, blank=True)

    marca=models.ForeignKey(Marca, on_delete=models.CASCADE)
    unidade_medida=models.ForeignKey(UnidadeMedida, on_delete=models.CASCADE)
    subcategoria=models.ForeignKey(SubCategoria, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.descricao)

    def save(self):
        self.descricao = self.descricao.upper()
        super(Produto, self).save()

    class Meta:
        verbose_name_plural='Produtos'
        unique_together=('codigo', 'codigo_barra')
    