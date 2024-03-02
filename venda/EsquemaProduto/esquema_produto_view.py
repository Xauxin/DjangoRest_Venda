from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from .esquema_produto_model import EsquemaProduto
from .esquema_produto_serializer import EsquemaProdutoSerializer
from estoque.Suprimentos.suprimento_view import Suprimento, SuprimentoSerializer

class EsquemaProdutoViewset(viewsets.ModelViewSet):
    queryset  = EsquemaProduto.objects.all()
    serializer_class = EsquemaProdutoSerializer

    