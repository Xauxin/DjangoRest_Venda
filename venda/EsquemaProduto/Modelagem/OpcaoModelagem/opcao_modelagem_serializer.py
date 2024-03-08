from rest_framework import serializers

from venda.EsquemaProduto.Modelagem.modelagem_model import Modelagem
from .opcao_modelagem_model import OpcaoModelagem

class OpcaoModelagemSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=50)
    valor= serializers.FloatField()
    modelagem = serializers.PrimaryKeyRelatedField(queryset=Modelagem.objects.all())

    def to_representation_modelagem(self, instance):
        return instance.nome