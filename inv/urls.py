from django.urls import path

from .views import CategoriaView, CategoriaNew, CategoriaEdit, CategoriaDel, \
    SubCategoriaView, SubCategoriaNew, SubCategoriaEdit, SubCategoriaDel, \
    MarcaView, MarcaNew, MarcaEdit, marca_desativar, \
    UnidadeMedidaView, UnidadeMedidaNew, UnidadeMedidaEdit, unidade_medida_desativar, \
    ProdutoView, ProdutoNew, ProdutoEdit, produto_desativar

urlpatterns = [
    path('categorias/', CategoriaView.as_view(), name='categoria_list'),
    path('categorias/new', CategoriaNew.as_view(), name='categoria_new'),
    path('categorias/edit/<int:pk>', CategoriaEdit.as_view(), name='categoria_edit'),
    path('categorias/delete/<int:pk>', CategoriaDel.as_view(), name='categoria_del'),
    path('subcategorias/', SubCategoriaView.as_view(), name='subcategoria_list'),
    path('subcategorias/new', SubCategoriaNew.as_view(), name='subcategoria_new'),
    path('subcategorias/edit/<int:pk>', SubCategoriaEdit.as_view(), name='subcategoria_edit'),
    path('subcategorias/delete/<int:pk>', SubCategoriaDel.as_view(), name='subcategoria_del'),
    path('marca/', MarcaView.as_view(), name='marca_list'),
    path('marca/new', MarcaNew.as_view(), name='marca_new'),
    path('marca/edit/<int:pk>', MarcaEdit.as_view(), name='marca_edit'),
    path('marca/desativar/<int:id>', marca_desativar, name='marca_desativar'),

    path('um/', UnidadeMedidaView.as_view(), name='um_list'),
    path('um/new', UnidadeMedidaNew.as_view(), name='um_new'),
    path('um/edit/<int:pk>', UnidadeMedidaEdit.as_view(), name='um_edit'),
    path('um/desativar/<int:id>', unidade_medida_desativar, name='um_desativar'),
    
    path('produto/', ProdutoView.as_view(), name='produto_list'),
    path('produto/new', ProdutoNew.as_view(), name='produto_new'),
    path('produto/edit/<int:pk>', ProdutoEdit.as_view(), name='produto_edit'),
    path('produto/desativar/<int:id>', produto_desativar, name='produto_desativar'),
]
