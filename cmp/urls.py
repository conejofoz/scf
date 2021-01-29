from django.urls import path, include

from .views import FornecedorView, FornecedorNew, FornecedorEdit, \
    fornecedor_desativar, ComprasView, compras, CompraDetDelete

from .reportes import reporte_compras, imprimir_compra

urlpatterns = [
    path('fornecedores/', FornecedorView.as_view(), name='fornecedor_list'),
    path('fornecedores/new', FornecedorNew.as_view(), name='fornecedor_new'),
    path('fornecedores/edit/<int:pk>', FornecedorEdit.as_view(), name='fornecedor_edit'),
    path('fornecedores/desativar/<int:id>', fornecedor_desativar, name='fornecedor_desativar'),

    path('compras/', ComprasView.as_view(), name='compras_list'),
    path('compras/new', compras, name='compras_new'),
    path('compras/edit/<int:compra_id>', compras, name='compras_edit'),
    path('compras/<int:compra_id>/delete/<int:pk>', CompraDetDelete.as_view(), name='compras_del'),

    path('compras/lista', reporte_compras, name='compras_print_all'),
    path('compras/<int:compra_id>/imprimir', imprimir_compra, name='compras_print_one'),
]
