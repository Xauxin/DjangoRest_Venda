from random import choices
from xml.dom import ValidationErr
from rest_framework import serializers
from venda.EsquemaProduto.Modelagem.OpcaoModelagem.opcao_modelagem_serializer import OpcaoModelagemSerializer, OpcaoModelagem
from venda.EsquemaProduto.esquema_produto_model import EsquemaProduto
from .modelagem_model import Modelagem

class ModelagemSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=50)
    requerido = serializers.BooleanField()
    tipo = serializers.ChoiceField(choices=Modelagem.TIPOS)
    esquema_produto = serializers.PrimaryKeyRelatedField(queryset=EsquemaProduto.objects.all(), many=False)
    opcoes_modelagem = serializers.DictField(allow_null=True)

    def to_representation(self, instance):
        opcoes = OpcaoModelagem.objects.filter(modelagem = instance.id)
        list_opcoes = list()
        for opcao in opcoes:
            list_opcoes.append((OpcaoModelagemSerializer().to_representation_modelagem(opcao)))
        return {
            'nome' : instance.nome,
            'requerido':('requerido' if instance.requerido else 'Não requerido'),
            'tipo' : instance.get_tipo_display(),
            'opcoes': list_opcoes
        }

    def to_representation_esquema_produto(self, instance):
        opcoes = OpcaoModelagem.objects.filter(modelagem = instance.id)
        list_opcoes = list()
        for opcao in opcoes:
            list_opcoes.append((OpcaoModelagemSerializer().to_representation_modelagem(opcao)))
        return {
            'nome' : instance.nome,
            'opcoes': list_opcoes
        }

    def create(self, validated_data):
        validated_data_opcoes = validated_data.pop('opcoes_modelagem', None)
        print(validated_data_opcoes)
        modelagem = Modelagem.objects.create(**validated_data)
        for key, value in validated_data_opcoes.items():
            OpcaoModelagem.objects.create(nome=key, valor=value, modelagem=modelagem)
        modelagem.save()
        return modelagem

    



    # nome = models.CharField(max_length=50, blank=False, null=False)
    # requerido = models.BooleanField()
    # tipo = models.CharField(max_length= 1, choices=TIPOS)
    # esquema_produto = models.ForeignKey('EsquemaProduto', on_delete=models.CASCADE, null=False, blank=False, related_name='+')