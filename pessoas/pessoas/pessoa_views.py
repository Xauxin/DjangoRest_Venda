from rest_framework.response import Response
from rest_framework import viewsets, status
from .pessoa_serializer import Pessoa, PessoaSerializer

class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        objeto = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data , status=status.HTTP_201_CREATED, headers=headers)

class NucleoComParticoesPorPessoaViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        pk = self.kwargs.get('pk', "")
        pk_list = self.kwargs.get('pk_list', "")
        if pk:
            return Pessoa.objects.get(id=self.kwargs['pk'])
        if pk_list:
            print(self.kwargs['pk_list'])
    serializer_class = PessoaSerializer

    def list(self, request, *args, **kwargs):
        print(kwargs['pk_list'])
        print('oi')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        pessoa = self.get_queryset()
        print(pessoa)
        return super().retrieve(request, *args, **kwargs)
        
