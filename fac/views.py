from django.shortcuts import render, redirect
from django.views import generic

#se ussa com formularios
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

#autenticação de django
from django.contrib.auth import authenticate

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import Cliente, FaturaEnc, FaturaDet
from .forms import ClienteForm
import inv.views as inv
from inv.models import Produto


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
@permission_required('fac.change_faturaenc', login_url='bases:sem_privilegios')
def faturas(request, id=None):
    template_name='fac/faturas.html'

    

    detalhe = {

    }

    clientes = Cliente.objects.filter(estado=True)

    #quando é carregada a página
    if request.method == 'GET':
        enc = FaturaEnc.objects.filter(pk=id).first()
        # se a fatura não existe reinicia-la
        if not enc:
            cabecalho = {
                'id':0,
                'data':datetime.today(),
                'cliente':0,
                'sub_total':0.00,
                'desconto':0.00,
                'total':0.00
            }
            detalhe=None
        # se existe a fatura
        else:
            cabecalho = {
                'id':enc.id,
                'data':enc.data,
                'cliente':enc.cliente,
                'sub_total':enc.sub_total,
                'desconto':enc.desconto,
                'total':enc.total
            }
            detalhe=FaturaDet.objects.filter(fatura=enc)

        #movido para dentro do métido get para evitar problema
        contexto={"enc": cabecalho, "det": detalhe, "clientes":clientes}
    

    # quando salva a fatura
    if request.method == 'POST':
        cliente = request.POST.get('enc_cliente')
        data = request.POST.get('data')
        cli = Cliente.objects.get(pk=cliente)

        #se não existir o id é pq a fatura é nova
        if not id:
            enc = FaturaEnc(
                cliente = cli,
                data=data
            )
            if enc:
                enc.save()
                id = enc.id
        # se existe id é pq já tem a fatura
        else:
            enc = FaturaEnc.objects.filter(pk=id).first()
            if enc:
                #se a fatura existe o único que pode ser mudado é o cliente
                enc.cli = cli
                enc.save()


        #se chegou até esse ponto sem número de fatura é pq tem erro
        if not id:
            messages.error(request, 'Não é possível continuar, erro com número de fatura')
            return redirect("fac:fatura_list")


        # se chegou até aqui é pq tudo esta bem e vai ser gravado o detalhe
        # nesse sistema o detalhe é adicionado um a um
        codigo = request.POST.get("codigo")
        quantidade = request.POST.get("quantidade")
        preco = request.POST.get("preco")
        s_total = request.POST.get("sub_total_detalhe")
        desconto = request.POST.get("desconto_detalhe")
        total = request.POST.get("total_detalhe")

        #criar um objeto produto com o código vindo do formulário
        prod = Produto.objects.get(codigo=codigo)

        #inicializar detalhe
        det = FaturaDet(
            fatura = enc,
            produto = prod,
            quantidade = quantidade,
            preco = preco,
            sub_total=s_total,
            desconto=desconto,
            total=total
        )

        #se conseguiu criar o detalhe aogra é só salvar
        if det:
            det.save()

        #depois de salvar voltar a mesma pagina passando o id da fatura
        # daí cai no método get e ele consulta a fatura poe na tela para adicionar outro produto
        return redirect("fac:fatura_edit", id=id)

    return render(request, template_name, contexto)


class ProdutoView(inv.ProdutoView):
    template_name="fac/buscar_produto.html"


def apagar_detalhe_fatura(request, id):
    template_name = "fac/fatura_apagar_detalhe.html"

    det = FaturaDet.objects.get(pk=id)

    if request.method == 'GET':
        contexto = {"det":det}


    if request.method == 'POST':
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user = authenticate(username=usr, password=pas)

        if not user:
            return HttpResponse("Usuário ou senha incorretos")

        if not user.is_active:
            return HttpResponse("Usuário desativado")

        if user.is_superuser or user.has_perm("fac.sup_caixa_faturadet"):
            det.id = None
            det.quantidade = (-1 * det.quantidade)
            det.sub_total = (-1 * det.sub_total)
            det.desconto = (-1 * det.desconto)
            det.total = (-1 * det.total)
            det.save()

            return HttpResponse("ok")

        return HttpResponse("Usuário não autorizado")
            


    return render(request, template_name, contexto)
