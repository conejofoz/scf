from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy
import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

#import para poder trabalhar com ajax
from django.http import HttpResponse
import json
from django.db.models import Sum


from .models import Fornecedor, ComprasDet, ComprasEnc
from cmp.forms import FornecedorForm, ComprasEncForm

from inv.models import Produto

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


class ComprasView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = ComprasEnc
    template_name="cmp/compras_list.html"
    context_object_name="obj"
    permission_required='cmp.view_comprasenc'


@login_required(login_url='/login/') #decorator
@permission_required('cmp.view_comprasenc', login_url='bases:sem_privilegios')
def compras(request, compra_id=None):
    template_name="cmp/compras.html"
    prod=Produto.objects.filter(estado=True)
    form_compras={}
    contexto={}

    if request.method == 'GET':
        print('entrou no get')
        form_compras = ComprasEncForm()
        enc = ComprasEnc.objects.filter(pk=compra_id).first()

        if enc:
            det = ComprasDet.objects.filter(compra=enc)
            data_compra = datetime.date.isoformat(enc.data_compra)
            data_fatura = datetime.date.isoformat(enc.data_fatura)

            e={
                'data_compra': data_compra,
                'fornecedor': enc.fornecedor,
                'observacao': enc.observacao,
                'no_fatura': enc.no_fatura,
                'data_fatura': enc.data_fatura,
                'sub_total': enc.sub_total,
                'desconto': enc.desconto,
                'total': enc.total
            }

            form_compras = ComprasEncForm(e)

        else: 
            det = None

        contexto = {'produtos': prod, 'cabecalho': enc, 'detalhe': det, 'form_enc': form_compras}

    if request.method == 'POST':
        print('entrou no post')
        print(request.POST)
        data_compra=request.POST.get('data_compra')
        observacao=request.POST.get('observacao')
        no_fatura=request.POST.get('no_fatura')
        data_fatura=request.POST.get('data_fatura')
        fornecedor=request.POST.get('fornecedor')
        sub_total=0
        desconto=0
        total=0

        if not compra_id:
            print('entrou no nova compra')
            forn=Fornecedor.objects.get(pk=fornecedor)

            enc = ComprasEnc(
                data_compra=data_compra,
                observacao=observacao,
                no_fatura=no_fatura,
                data_fatura=data_fatura,
                fornecedor=forn,
                uc=request.user
            )

            print('enc: ', enc)

            if enc:
                enc.save()
                compra_id=enc.id
                print('salvou a compra ', compra_id)
            else:
                print('Não salvou a nova compra')
        else:
            print('a compra ja existe')
            enc=ComprasEnc.objects.filter(pk=compra_id).first()
            if enc:
                enc.data_compra=data_compra
                enc.observacao=observacao
                enc.no_fatura=no_fatura
                enc.data_fatura=data_fatura
                enc.um=request.user.id
                enc.save()

        if not compra_id:
            return redirect("cmp:compras_list")


        produto = request.POST.get("id_id_produto")
        quantidade = request.POST.get("id_quantidade_detalhe")
        preco = request.POST.get("id_preco_detalhe")
        sub_total_detalhe = request.POST.get("id_sub_total_detalhe")
        desconto_detalhe = request.POST.get("id_desconto_detalhe")
        total_detalhe=request.POST.get("id_total_detalhe")

        prod = Produto.objects.get(pk=produto)

        det = ComprasDet(
            compra=enc,
            produto=prod,
            quantidade=quantidade,
            preco_forn=preco,
            desconto=desconto_detalhe,
            custo=0,
            uc=request.user,
        )

        if det:
            det.save()
            sub_total=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            desconto=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('desconto'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.desconto = desconto["desconto__sum"]
            enc.save()

        return redirect("cmp:compras_edit", compra_id=compra_id)

    return render(request, template_name, contexto)


class CompraDetDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "cmp.delete_comprasdet"
    model = ComprasDet
    template_name = "cmp/compras_det_del.html"
    context_object_name = 'obj'
    
    def get_success_url(self):
          compra_id=self.kwargs['compra_id']
          return reverse_lazy('cmp:compras_edit', kwargs={'compra_id': compra_id})