from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

#import para poder trabalhar com ajax
from django.http import HttpResponse
import json

from .models import Fornecedor
from cmp.forms import FornecedorForm

class FornecedorView(LoginRequiredMixin, generic.ListView):
    model=Fornecedor
    template_name='cmp/fornecedor_list.html'
    context_object_name='obj'
    login_url='bases:login'

class FornecedorNew(LoginRequiredMixin, generic.CreateView):
    model=Fornecedor
    template_name='cmp/fornecedor_form.html'
    context_object_name='obj'
    form_class=FornecedorForm
    success_url=reverse_lazy('cmp:fornecedor_list')
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class FornecedorEdit(LoginRequiredMixin, generic.UpdateView):
    model=Fornecedor
    template_name='cmp/fornecedor_form.html'    
    context_object_name='obj'
    form_class=FornecedorForm
    success_url=reverse_lazy('cmp:fornecedor_list')
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


def fornecedor_desativar(request, id):
    template_name = 'cmp/desativar_forn.html'
    contexto={}

    fornecedor = Fornecedor.objects.filter(pk=id).first()

    if not fornecedor:
        return HttpResponse('Fornecedor não existe' + str(id))

    if request.method == 'GET':
        contexto={'obj':fornecedor}

    if request.method == 'POST':
        fornecedor.estado = False
        contexto={'obj':'OK'}
        fornecedor.save()
        return HttpResponse('Fornecedor desativado')


    return render(request,template_name,contexto)