from django import forms

from .models import Categoria

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