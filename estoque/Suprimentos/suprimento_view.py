from rest_framework import viewsets
from .suprimento_serializer import SuprimentoSerializer
from .suprimento_model import Suprimento

class SuprimentoViewset(viewsets.ModelViewSet):
    queryset = Suprimento.objects.all()
    serializer_class = SuprimentoSerializer