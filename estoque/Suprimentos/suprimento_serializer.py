from rest_framework import serializers
from .suprimento_model import Suprimento
from .Cores.cores_model import Cor

class SuprimentoSerializer(serializers.Serializer):
    
    nome = serializers.CharField(max_length=35)
    valor = serializers.FloatField()
    unidade_de_medida = serializers.ChoiceField(choices=Suprimento.UNIDADES_MEDIDAS)
    classificacao = serializers.ChoiceField(choices=Suprimento.CLASSES)
    cores = serializers.PrimaryKeyRelatedField(queryset=Cor.objects.all(), many=True)


    def get_unidade_de_medida(self, obj):
        return obj.get_unidade_de_medida_display()

    def get_classificacao(self, obj):
        return obj.get_classificacao_display()

    def to_representation(self, instance):
        return {
            'nome': instance.nome
        }

    def to_representation_esquema_produto(self, instance):
        return  instance.nome
      

    def create(self, validated_data):
        validated_data_suprimento = validated_data.pop('cores')
        suprimento = Suprimento.objects.create(**validated_data)
        print(validated_data, type(validated_data_suprimento))
        suprimento.cores.set(objs=validated_data_suprimento)
        suprimento.save()
        return suprimento

    def update(self, instance):
        super().update(self, instance)
