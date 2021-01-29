from django import forms

from .models import Fornecedor, ComprasEnc

class FornecedorForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model=Fornecedor
        exclude=['um', 'fm', 'uc', 'fc']
        widget={'descricao':forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ComprasEncForm(forms.ModelForm):
    data_compra = forms.DateInput()
    data_fatura = forms.DateInput()

    class Meta:
        model=ComprasEnc
        fields=[
            'fornecedor', 'data_compra', 'observacao', 'no_fatura', 'data_fatura',
            'sub_total', 'desconto', 'total'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['data_compra'].widget.attrs['readonly'] = True
        self.fields['data_fatura'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['desconto'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True