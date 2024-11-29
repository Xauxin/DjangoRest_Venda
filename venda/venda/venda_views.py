from rest_framework.response import Response
from rest_framework import viewsets, status
from .venda_serializer import Venda, VendaSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        try:
            id_venda = kwargs['pk']
            modelo = Venda.objects.get(id = id_venda)
            modelo = serializer.detailed_to_representation(modelo)
        except Venda.DoesNotExist as e:
            return Response(f"Id: {kwargs['pk']} não existe em Esquema Produto", status=status.HTTP_404_NOT_FOUND)
        
        return Response(modelo, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        objeto = serializer.save()
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.detailed_to_representation(objeto) , status=status.HTTP_201_CREATED, headers=headers)
            

    def update(self, request, *args, **kwargs):
        try:
            esquema = Venda.objects.get(id = kwargs['pk'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
            if serializer.errors:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            updated = serializer.update(esquema, request.data)
        except Venda.DoesNotExist as e:
            return Response(f"Id: {kwargs['pk']} não existe em Esquema Produto", status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.detailed_to_representation(updated), status=status.HTTP_200_OK)

    
    
    def partial_update(self, request, *args, **kwargs):
        try:
            esquema = Venda.objects.get(id = kwargs['pk'])
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid()
            if serializer.errors:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            updated = serializer.update(esquema , request.data)
        except Venda.DoesNotExist as e:
            return Response(f"Id: {kwargs['pk']} não existe em Esquema Produto", status=status.HTTP_404_NOT_FOUND)   
        return Response(serializer.detailed_to_representation(updated), status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)