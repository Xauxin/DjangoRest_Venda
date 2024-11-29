from rest_framework import viewsets

from .tamanhos_model import Tamanho
from .tamanhos_serializer import TamanhoSerializer

class TamanhoViewset(viewsets.ModelViewSet):
    queryset  = Tamanho.objects.all()
    serializer_class = TamanhoSerializer

    def create(self, request, *args, **kwargs):
        print(request.body)
        return super().create(request, *args, **kwargs)