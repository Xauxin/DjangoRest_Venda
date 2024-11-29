from rest_framework import viewsets
from .medidas_model import Medida 
from .medidas_serializer import MedidaSerializer

class MedidaViewset(viewsets.ModelViewSet):
    queryset  = Medida.objects.all()
    serializer_class = MedidaSerializer

    
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)