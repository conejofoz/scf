from django.urls import path, include

from .views import FornecedorView, FornecedorNew, FornecedorEdit, \
    fornecedor_desativar

urlpatterns = [
    path('fornecedores/', FornecedorView.as_view(), name='fornecedor_list'),
    path('fornecedores/new', FornecedorNew.as_view(), name='fornecedor_new'),
    path('fornecedores/edit/<int:pk>', FornecedorEdit.as_view(), name='fornecedor_edit'),
    path('fornecedores/desativar/<int:id>', fornecedor_desativar, name='fornecedor_desativar'),
]
