from django import forms

from .models import Categoria, SubCategoria, Marca, UnidadeMedida, Produto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields=['descricao', 'estado']
        labels={'descricao':'Descrição', 'estado':'Estado'}
        widget={'descricao':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})


class SubCategoriaForm(forms.ModelForm):
    """
    impedir que as categorias inativas apareçam na lista para serem selecionadas
    para isso sobrescrever o queryset de categorias
    """
    categoria=forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True)
        .order_by('descricao')
    )
    class Meta:
        model=SubCategoria
        fields=['categoria', 'descricao', 'estado']
        labels={'descricao':'Sub Categoria', 'estado':'Estado'}
        widget={'descricao':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})   
        self.fields['categoria'].empty_label = "Selecione um Categoria"     


class MarcaForm(forms.ModelForm):
    class Meta:
        model=Marca
        fields=['descricao', 'estado']
        labels={'descricao':'Descrição', 'estado':'Estado'}
        widget={'descricao':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})            


class UnidadeMedidaForm(forms.ModelForm):
    class Meta:
        model=UnidadeMedida
        fields=['descricao', 'estado']
        labels={'descricao':'Descrição', 'estado':'Estado'}
        widget={'descricao':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})   


class ProdutoForm(forms.ModelForm):
    class Meta:
        model=Produto
        fields=['codigo','codigo_barra','descricao', 'estado', 'preco', \
            'existencia', 'ultima_compra', 'marca', 'subcategoria', 'unidade_medida']
        exclude=['um', 'fm', 'uc', 'fc']    
        #labels={'descricao':'Descrição', 'estado':'Estado'}
        widget={'descricao':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})       

        self.fields['ultima_compra'].widget.attrs['readonly'] = True      
        self.fields['existencia'].widget.attrs['readonly'] = True      