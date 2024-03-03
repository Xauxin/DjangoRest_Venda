from rest_framework import serializers
from .esquema_produto_model import EsquemaProduto
from .Medidas.medidas_serializer import MedidaSerializer, Medida 
from estoque.Suprimentos.suprimento_serializer import  Suprimento

class EsquemaProdutoSerializer(serializers.Serializer):
        nome = serializers.CharField(max_length=50)
        suprimentos = serializers.PrimaryKeyRelatedField(queryset=Suprimento.objects.all(), many=True)
        locais_de_bordado_sugeridos = serializers.CharField(max_length=50)
        valor_base = serializers.FloatField()

        def to_representation(self, instance):
             suprimentos = instance.suprimentos
             print(suprimentos)
             return {
                  instance.nome
             }

        def create(self, validated_data):
            validated_data_suprimento = validated_data.pop('suprimentos')
            esquema_produto = EsquemaProduto.objects.create(**validated_data)
            esquema_produto.suprimentos.set(validated_data_suprimento)
            return esquema_produto


        def update(self, instance):
            super().update(self, instance)