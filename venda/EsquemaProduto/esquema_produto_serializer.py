from rest_framework import serializers
from .esquema_produto_model import EsquemaProduto
from estoque.Suprimentos.suprimento_serializer import  Suprimento

class EsquemaProdutoSerializer(serializers.Serializer):
        model = EsquemaProduto
        nome = serializers.CharField(max_length=50)
        suprimento = serializers.PrimaryKeyRelatedField(queryset=Suprimento.objects.all(), many=True)
        locais_de_bordado_sugeridos = serializers.CharField(max_length=50)
        valor_base = serializers.FloatField()

        def create(self, validated_data):
            return EsquemaProduto.objects.create(**validated_data)