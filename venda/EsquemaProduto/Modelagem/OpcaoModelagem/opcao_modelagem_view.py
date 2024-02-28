from rest_framework import viewsets
from .opcao_modelagem_model import OpcaoModelagem
from .opcao_modelagem_serializer import OpcaoModelagemSerializer

class ModelagemViewset(viewsets.ModelViewSet):
    queryset  = OpcaoModelagem.objects.all()
    serializer_class = OpcaoModelagemSerializer