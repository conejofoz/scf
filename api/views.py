from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import ProdutoSerializer
from inv.models import Produto

from django.db.models import Q


class ProdutoList(APIView):
    def get(self,request):
       prod = Produto.objects.all()
       data =  ProdutoSerializer(prod,many=True).data
       return Response(data)


class ProdutoDetalhe(APIView):
    def get(self,request,codigo):
        #prod = get_object_or_404(Produto,codigo=codigo)
        prod = get_object_or_404(Produto, Q(codigo=codigo)|Q(codigo_barra=codigo))
        data = ProdutoSerializer(prod).data
        return Response(data)