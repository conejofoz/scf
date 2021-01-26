from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from .models import Categoria, SubCategoria, Marca, UnidadeMedida, Produto
from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, UnidadeMedidaForm, ProdutoForm

from bases.views import SemPrivilegios

class CategoriaView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "inv.view_categoria"
    model = Categoria
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class CategoriaNew(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model=Categoria
    template_name='inv/categoria_form.html'
    context_object_name="obj"
    form_class=CategoriaForm
    success_url=reverse_lazy("inv:categoria_list")
    login_url="bases:login"
    success_message="Categoria criada com sucesso!"

    def form_valid(self, form):
        form.instance.uc = self.request.user #está relacionado na tabela
        return super().form_valid(form)


class CategoriaEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model=Categoria
    template_name='inv/categoria_form.html'
    context_object_name='obj'
    form_class=CategoriaForm
    success_url=reverse_lazy("inv:categoria_list")
    login_url='bases:login'
    success_message="Categoria atualizada com sucesso!"

    def form_valid(self, form):
        form.instance.um = self.request.user.id #aqui não está relacionado por isso o id
        return super().form_valid(form)


class CategoriaDel(LoginRequiredMixin, generic.DeleteView):
    model=Categoria
    template_name='inv/catalogos_del.html'
    context_object_name="obj"
    success_url=reverse_lazy('inv:categoria_list')


class SubCategoriaView(LoginRequiredMixin, SemPrivilegios, generic.ListView):
    permission_required="inv.view_subcategoria"
    model=SubCategoria
    template_name="inv/subcategoria.html"
    context_object_name="obj"
    login_url="bases:login"


class SubCategoriaNew(LoginRequiredMixin, generic.CreateView):
    model=SubCategoria
    template_name='inv/subcategoria_form.html'
    context_object_name="obj"
    form_class=SubCategoriaForm
    success_url=reverse_lazy("inv:subcategoria_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user #está relacionado na tabela
        return super().form_valid(form)


class SubCategoriaEdit(LoginRequiredMixin, generic.UpdateView):
    model=SubCategoria
    template_name='inv/subcategoria_form.html'
    context_object_name="obj"
    form_class=SubCategoriaForm
    success_url=reverse_lazy('inv:subcategoria_list')
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class SubCategoriaDel(LoginRequiredMixin, generic.DeleteView):
    model=SubCategoria
    template_name='inv/catalogos_del.html'        
    context_object_name="obj"
    success_url=reverse_lazy('inv:subcategoria_list')


class MarcaView(LoginRequiredMixin, generic.ListView):
    model=Marca
    template_name='inv/marca_list.html'
    context_object_name='obj'    
    login_url='bases:login'


class MarcaNew(LoginRequiredMixin, generic.CreateView):
    model=Marca
    template_name='inv/marca_form.html'    
    context_object_name='obj'
    form_class=MarcaForm
    success_url=reverse_lazy('inv:marca_list')
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class MarcaEdit(LoginRequiredMixin, generic.UpdateView):
    model=Marca
    context_object_name='obj'
    form_class=MarcaForm
    success_url=reverse_lazy('inv:marca_list')        
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inv.change_marca', login_url='bases:sem_privilegios')
def marca_desativar(request, id):
    marca = Marca.objects.filter(pk=id).first()
    contexto={}
    template_name='inv/catalogos_del.html'

    if not marca:
        return redirect('inv:marca_list')

    if request.method=='GET':
        contexto={'obj':marca}

    if request.method=='POST':
        marca.estado=False
        marca.save()
        messages.success(request, 'Marca desativada!')
        return redirect('inv:marca_list')

    return render(request, template_name, contexto)

    
class UnidadeMedidaView(LoginRequiredMixin, generic.ListView):
    model=UnidadeMedida
    template_name='inv/um_list.html'
    context_object_name='obj'    
    login_url='bases:login'


class UnidadeMedidaNew(LoginRequiredMixin, generic.CreateView):
    model=UnidadeMedida
    template_name='inv/um_form.html'    
    context_object_name='obj'
    form_class=UnidadeMedidaForm
    success_url=reverse_lazy('inv:um_list')
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class UnidadeMedidaEdit(LoginRequiredMixin, generic.UpdateView):
    model=UnidadeMedida
    template_name='inv/um_form.html'
    context_object_name='obj'
    form_class=UnidadeMedidaForm
    success_url=reverse_lazy('inv:um_list')        
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


def unidade_medida_desativar(request, id):
    um = UnidadeMedida.objects.filter(pk=id).first()
    contexto={}
    template_name='inv/catalogos_del.html'

    if not um:
        return redirect('inv:um_list')

    if request.method=='GET':
        contexto={'obj':um}

    if request.method=='POST':
        um.estado=False
        um.save()
        return redirect('inv:um_list')

    return render(request, template_name, contexto)

    
class ProdutoView(LoginRequiredMixin, generic.ListView):
    model=Produto
    template_name='inv/produto_list.html'
    context_object_name='obj'    
    login_url='bases:login'


class ProdutoNew(LoginRequiredMixin, generic.CreateView):
    model=Produto
    template_name='inv/produto_form.html'    
    context_object_name='obj'
    form_class=ProdutoForm
    success_url=reverse_lazy('inv:produto_list')
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class ProdutoEdit(LoginRequiredMixin, generic.UpdateView):
    model=Produto
    template_name='inv/produto_form.html' 
    context_object_name='obj'
    form_class=ProdutoForm
    success_url=reverse_lazy('inv:produto_list')        
    login_url='bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


def produto_desativar(request, id):
    um = Produto.objects.filter(pk=id).first()
    contexto={}
    template_name='inv/catalogos_del.html'

    if not um:
        return redirect('inv:produto_list')

    if request.method=='GET':
        contexto={'obj':um}

    if request.method=='POST':
        um.estado=False
        um.save()
        return redirect('inv:produto_list')

    return render(request, template_name, contexto)

    

