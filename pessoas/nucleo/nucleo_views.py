from rest_framework.response import Response
from rest_framework import viewsets, status

from pessoas.pessoas.pessoa_model import Pessoa
from .nucleo_serializer import Nucleo, NucleoSerializer

class NucleoViewSet(viewsets.ModelViewSet):
    queryset = Nucleo.objects.all()
    serializer_class = NucleoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        objeto = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data , status=status.HTTP_201_CREATED, headers=headers)

class NucleoComParticoesViewSet(viewsets.ModelViewSet):
    queryset = Nucleo.objects.all()
    serializer_class = NucleoSerializer

    def list(self, request, *args, **kwargs):
        nucleos = self.queryset
        serializer = self.get_serializer()
        response_data = {}
        for nucleo in nucleos:
            response_data |= serializer.to_representation_com_particao(nucleo)
        return Response(response_data, status=status.HTTP_200_OK)
