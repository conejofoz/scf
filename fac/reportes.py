from django.shortcuts import render
from django.utils.dateparse import parse_date
from datetime import timedelta

from .models import FaturaEnc,FaturaDet

def imprimir_fatura_recibo(request,id):
    template_name="fac/fatura_one.html"

    enc = FaturaEnc.objects.get(id=id)
    det = FaturaDet.objects.filter(fatura=id)

    context={
        'request':request,
        'enc':enc,
        'detalle':det
    }

    return render(request,template_name,context)

""" def imprimir_factura_list(request,f1,f2):
    template_name="fac/facturas_print_all.html"

    f1=parse_date(f1)
    f2=parse_date(f2)
    f2=f2 + timedelta(days=1)

    enc = FacturaEnc.objects.filter(fecha__gte=f1,fecha__lt=f2)
    f2=f2 - timedelta(days=1)
    
    context = {
        'request':request,
        'f1':f1,
        'f2':f2,
        'enc':enc
    }

    return render(request,template_name,context) """