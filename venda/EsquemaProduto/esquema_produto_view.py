from rest_framework import viewsets
from .esquema_produto_model import EsquemaProduto
from .esquema_produto_serializer import EsquemaProdutoSerializer

class EsquemaProdutoViewset(viewsets.ModelViewSet):
    queryset  = EsquemaProduto.objects.all()
    serializer_class = EsquemaProdutoSerializer