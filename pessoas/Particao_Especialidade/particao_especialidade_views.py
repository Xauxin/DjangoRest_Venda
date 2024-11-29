from rest_framework.response import Response
from rest_framework import viewsets, status

from pessoas.pessoas.pessoa_model import Pessoa
from .particao_especialidade_serializer import Particao_Especialidade, Particao_EspecialidadeSerializer

class Particao_especialidadeViewSet(viewsets.ModelViewSet):
    queryset = Particao_Especialidade.objects.all()
    serializer_class = Particao_EspecialidadeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        objeto = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data , status=status.HTTP_201_CREATED, headers=headers)

class Particao_especialidade_por_nucleoViewSet(viewsets.ModelViewSet):
    serializer_class = Particao_EspecialidadeSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return Response(serializer.to_representation_por_nucleo(), status=status.HTTP_200_OK)