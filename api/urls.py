from django.urls import path, include
from .views import ProdutoList, ProdutoDetalhe

urlpatterns = [
    path('v1/produtos/', ProdutoList.as_view(), name='produto_list'),
    path('v1/produtos/<str:codigo>', ProdutoDetalhe.as_view(), name='produto_detalhe'),
]
