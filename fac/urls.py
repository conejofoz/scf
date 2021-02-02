from django.urls import path, include

from .views import ClienteView, ClienteNew, ClienteEdit, clienteDesativar, FaturaView, faturas, ProdutoView

urlpatterns = [
    path('clientes/', ClienteView.as_view(), name='cliente_list'),
    path('clientes/new', ClienteNew.as_view(), name='cliente_new'),
    path('clientes/<int:pk>', ClienteEdit.as_view(), name='cliente_edit'),
    path('clientes/estado/<int:id>', clienteDesativar, name='cliente_desativar'),

    path('faturas/', FaturaView.as_view(), name="fatura_list"),
    path('faturas/new', faturas, name="fatura_new"),
    path('faturas/buscar-produto', ProdutoView.as_view(), name="fatura_produto"),
]
