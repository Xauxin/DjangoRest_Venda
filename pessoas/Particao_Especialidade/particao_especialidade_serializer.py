from rest_framework import serializers

from pessoas.pessoas.pessoa_model import Pessoa
from .particao_especialidade_model import Nucleo, Particao_Especialidade
from ..nucleo.nucleo_serializer import NucleoSerializer
from utils.validacoes.validacoes_gerais import *


class Particao_EspecialidadeSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=50)
    nucleo = serializers.PrimaryKeyRelatedField(queryset=Nucleo.objects.all())


    field_validators = {
        'nome' : lambda value: valida_string(value, 50, 1),
        'nucleo': lambda value: valida_chave_estrangeira(value, Nucleo)
    }

    def to_representation_por_pessoa(self, pessoa_instance):
        por_pessoa = {}
        nucleos = pessoa_instance.nucleos.all()
        particoes_especialidades = pessoa_instance.particoes_especialidades.all()
        for nucleo in nucleos:
            filtro = particoes_especialidades.filter(nucleo_id = nucleo.pk)
            por_pessoa[nucleo.nome] = [part.nome for part in filtro]
        return por_pessoa

    def to_representation_por_nucleo(self):
        por_nucleos = {}
        nucleos = Nucleo.objects.all()
        for nucleo in nucleos:
            filtro = Particao_Especialidade.objects.filter(nucleo_id = nucleo.pk)
            por_nucleos[nucleo.nome] = [part.nome for part in filtro]
        return por_nucleos

    def to_representation(self, instance):
        nucleo = NucleoSerializer().to_representation(instance.nucleo)
        return{
            'nome' : instance.nome,
            'nucleo' : nucleo['nome']
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
        nucleo = validated_data.pop('nucleo')
        particao_especilidade = Particao_Especialidade.objects.create(**validated_data, nucleo_id=nucleo[0].pk)
        particao_especilidade.save()
        return particao_especilidade