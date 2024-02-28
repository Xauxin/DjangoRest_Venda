from rest_framework import viewsets
from .cores_serializer import CorSerializer
from .cores_model import Cor

class CorViewset(viewsets.ModelViewSet):
    queryset = Cor.objects.all()
    serializer_class = CorSerializer