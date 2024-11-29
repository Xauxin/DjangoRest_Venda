from rest_framework import serializers
from .nucleo_model import Nucleo
from ..Particao_Especialidade.particao_especialidade_serializer import Particao_Especialidade
from utils.validacoes.validacoes_gerais import *


class NucleoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=50)
    abreviado = serializers.CharField(max_length=4)

    field_validators = {
        'nome' : lambda value: valida_string(value, 50, 1),
        'abreviado': lambda value: valida_string(value,4, 4)
    }

    def to_representation(self, instance):

        return super().to_representation(instance)

    def to_representation_com_particao(self, instance):
        particoes = Particao_Especialidade.objects.filter(nucleo_id = instance.pk)
        list_particoes = [particao.nome for particao in particoes]
        print(list_particoes)
        return {
            'nome' : instance.nome,
            'particoes' : list_particoes
        }

    def to_internal_value(self, data):
        errors = {}
        internal_value = {}

        for field, validator in self.field_validators.items():
            value = data.get(f'{field}')
            if not self.partial or value or value is not None:
                try:
                    internal_value[f'{field}'] = validator(value)
                except fieldError as e:
                    errors[f'{field}'] = e.msg
        if errors:
            raise serializers.ValidationError(errors)
        return internal_value


    def create(self, validated_data):
        nucleo = Nucleo.objects.create(**validated_data)
        nucleo.save()
        return nucleo