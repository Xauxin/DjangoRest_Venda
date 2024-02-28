from rest_framework import viewsets
from .modelagem_model import Modelagem
from .modelagem_serializer import ModelagemSerializer

class ModelagemViewset(viewsets.ModelViewSet):
    queryset  = Modelagem.objects.all()
    serializer_class = ModelagemSerializer