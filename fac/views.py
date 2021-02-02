from django.shortcuts import render
from django.views import generic

#se ussa com formularios
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import Cliente, FaturaEnc, FaturaDet
from .forms import ClienteForm
import inv.views as inv


class ClienteView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Cliente
    template_name='fac/cliente_list.html'
    context_object_name='obj'
    permission_required='fac.view_cliente'
    login_url='bases:login'


class VistaBaseCreate(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    context_object_name='obj'
    success_message="Registro inserido com sucesso!"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class VistaBaseEdit(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    context_object_name='obj'
    success_message="Registro atualizado com sucesso!"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ClienteNew(VistaBaseCreate):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url=reverse_lazy("fac:cliente_list")
    permission_required="fac.add_cliente"


class ClienteEdit(VistaBaseEdit):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url=reverse_lazy("fac:cliente_list")
    permission_required="fac.change_cliente"    


@login_required(login_url="/login/")
@permission_required("fac.change_cliente", login_url="/login/")
def clienteDesativar(request, id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method == "POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")    

    return HttpResponse("FAIL")    


class FaturaView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = FaturaEnc
    template_name = 'fac/fatura_list.html'
    context_object_name = "obj"
    permission_required="fac.view_faturaenc"


@login_required(login_url='/login/')
@permission_required('fac.change_faturasenc', login_url='bases:sem_privilegios')
def faturas(request, id=None):
    template_name='fac/faturas.html'

    cabecalho = {
        'data':datetime.today()
    }

    detalhe = {

    }

    clientes = Cliente.objects.filter(estado=True)

    contexto={"enc": cabecalho, "det": detalhe, "clientes":clientes}
    print(contexto)

    return render(request, template_name, contexto)


class ProdutoView(inv.ProdutoView):
    template_name="fac/buscar_produto.html"