from django import forms

from .models import Categoria, SubCategoria, Marca

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