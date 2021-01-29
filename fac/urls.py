from django.urls import path, include

from .views import ClienteView, ClienteNew, ClienteEdit, clienteDesativar

urlpatterns = [
    path('clientes/', ClienteView.as_view(), name='cliente_list'),
    path('clientes/new', ClienteNew.as_view(), name='cliente_new'),
    path('clientes/<int:pk>', ClienteEdit.as_view(), name='cliente_edit'),
    path('clientes/estado/<int:id>', clienteDesativar, name='cliente_desativar'),
]
