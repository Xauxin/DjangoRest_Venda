from rest_framework import serializers
from venda.EsquemaProduto.Modelagem.modelagem_serializer import ModelagemSerializer, Modelagem
from venda.EsquemaProduto.Tamanhos.tamanhos_serializer import TamanhoSerializer, Tamanho
from .esquema_produto_model import EsquemaProduto
from .Medidas.medidas_serializer import MedidaSerializer, Medida
from estoque.Suprimentos.suprimento_serializer import Suprimento, SuprimentoSerializer


class EsquemaProdutoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=50)
    suprimentos = serializers.PrimaryKeyRelatedField(queryset=Suprimento.objects.all(), many=True)
    medidas = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Medida.objects.all(), many=True, allow_empty=True))
    locais_de_bordado_sugeridos = serializers.CharField(max_length=50)
    valor_base = serializers.FloatField()

    def to_representation(self, instance):
        '''
        Desserialização da instancia em objeto JSON
        '''
        tamanhos = Tamanho.objects.all()
        list_tamanhos = list()
        for tamanho in tamanhos:
            list_tamanhos.append(TamanhoSerializer().to_representation_esquema_produto(tamanho))
        modelagens = Modelagem.objects.filter(esquema_produto=instance.id)
        list_modelagens = list()
        for modelagem in modelagens:
            list_modelagens.append((ModelagemSerializer().to_representation_esquema_produto(modelagem)))
        medidas = Medida.objects.filter(esquema_produto=instance.id)
        list_medidas= list()
        for medida in medidas:
            list_medidas.append((MedidaSerializer().to_representation_esquema_produto(medida)))
        suprimentos = instance.suprimentos.all()
        list_suprimento = list()
        for suprimento in suprimentos:
            list_suprimento.append((SuprimentoSerializer().to_representation_esquema_produto(suprimento)))
        return{
            "nome": instance.nome,
            'suprimentos': list_suprimento,
            'modelagens': list_modelagens,
            'tamanhos': list_tamanhos,
            'medidas': list_medidas,
            "locais_de_bordado_sugeridos": instance.locais_de_bordado_sugeridos,
            "valor_base": instance.valor_base
     }

    def create(self, validated_data):
        '''
        Crias os objetos de Esquema_produto
        Juntamente cria todas as dependencias
        '''
        validated_data_suprimento = validated_data.pop('suprimentos')
        esquema_produto = EsquemaProduto.objects.create(**validated_data)
        print(validated_data, type(validated_data_suprimento))
        esquema_produto.suprimentos.set(objs=validated_data_suprimento)
        esquema_produto.save()
        return esquema_produto

    def update(self, instance):
        super().update(self, instance)
