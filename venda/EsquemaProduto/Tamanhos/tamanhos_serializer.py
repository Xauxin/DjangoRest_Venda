from rest_framework import serializers
from venda.EsquemaProduto.esquema_produto_model import EsquemaProduto
from .tamanhos_model import Tamanho

class TamanhoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=3)
    complexidade = serializers.ChoiceField(Tamanho.COMPLEXIDADES)
    esquema_produto = serializers.PrimaryKeyRelatedField(queryset=EsquemaProduto.objects.all(), many=False)

    def to_representation_esquema_produto(self, instance):
        return instance.nome

    def create(self, validated_data):
        return Tamanho.objects.create(**validated_data)

    def get_complexidade(self, obj):
        return obj.get_complexidade_display()