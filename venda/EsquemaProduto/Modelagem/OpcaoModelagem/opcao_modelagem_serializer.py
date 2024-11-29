from rest_framework import serializers
from utils.validacoes.validacoes_gerais import *
from venda.EsquemaProduto.Modelagem.modelagem_model import Modelagem
from .opcao_modelagem_model import OpcaoModelagem

class OpcaoModelagemSerializer(serializers.Serializer):


    nome = serializers.CharField(max_length=50)
    valor= serializers.FloatField()
    modelagem = serializers.PrimaryKeyRelatedField(queryset=Modelagem.objects.all())

    validadores_de_campos = {
        'nome': lambda value: valida_string(value, 50 , 1),
        'valor': lambda value: valida_float(value),
    }

    

    def to_internal_value(self, data):
        errors = {}
        internal_value = {}
        for field, validator in self.validadores_de_campos.items():
            value = data.get(f'{field}', "")
            try:
                internal_value[field] = validator(value)
            except fieldError as e:
                errors[f'{field}'] = e.msg


        if errors:
            raise fieldError(errors)
        
        return internal_value
    
    def create(self, validated_data, modelagem_instance):
        return OpcaoModelagem.objects.create(
            **validated_data, modelagem_id=modelagem_instance.pk
        )

    def to_representation(self, instance):
        return instance.nome

    def detailed_to_representation(self, instance):
        return {
            instance.nome: instance.valor
        }

    