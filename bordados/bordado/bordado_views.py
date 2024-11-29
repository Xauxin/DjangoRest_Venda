from email.mime import image
from rest_framework.response import Response
from rest_framework import viewsets, status
from .bordado_serializer import Bordado, BordadoSerializer
from PIL import Image

class BordadoViewSet(viewsets.ModelViewSet):
    queryset = Bordado.objects.all()
    serializer_class = BordadoSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)   



