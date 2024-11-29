from rest_framework import serializers
from typing import Dict

from pessoas.pessoas.endereco.endereco_serializer import EnderecoSerializer
from .pessoa_model import Nucleo, Particao_Especialidade, Pessoa
from ..Particao_Especialidade.particao_especialidade_serializer import NucleoSerializer, Particao_EspecialidadeSerializer
from .endereco.endereco_model import Endereco
from utils.internalizadores.internalizadores_gerais import *
from utils.validacoes.validacoes_pessoas import *
from utils.validacoes.validacoes_gerais import *

class PessoaSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=50)
    nucleos = serializers.PrimaryKeyRelatedField(queryset=Nucleo.objects.all(), many=True)
    endereco = serializers.PrimaryKeyRelatedField(queryset=Endereco.objects.all())
    particoes_especialidades = serializers.PrimaryKeyRelatedField(queryset=Particao_Especialidade.objects.all(), many=True)
    classificacao = serializers.ChoiceField(choices=Pessoa.CLASSIFICACOES)
    telefone = serializers.CharField(max_length=13)
    cpf_cnpj = serializers.CharField(max_length=14)
    data_nascimento = serializers.DateField()
    status = serializers.CharField(max_length=13)

    fields_internalizer = {
        'nome' : lambda value: internaliza_string(value, 50, 1),
        'nucleos': lambda value: internaliza_chave_estrangeira(value, Nucleo),
        'particoes_especialidades' : lambda value: internaliza_chave_estrangeira(value, Particao_Especialidade),
        'endereco': lambda value: valida_endereco(value),
        'classificacao' : lambda value: internaliza_opcoes(value, Pessoa.CLASSIFICACOES),
        'telefone' : lambda value: valida_telefone(value),
        'cpf_cnpj' : lambda value: valida_cpf_cnpj(value),
        'data_nascimento' : lambda value: internaliza_data(value),
        'data_cadastro' : lambda value:internaliza_data(value)
    }

    fields_validation = ['nome', 'cpf_cnpj']

    fields_serializers :Dict[str, type[EnderecoSerializer]] = {
        'endereco': EnderecoSerializer,
    } 

    fields_models :Dict[str, type[Endereco]] = {
        'endereco': Endereco,
    } 

    def to_internal_value(self, data):
        errors = {}
        internal_value = {}
        for field, validator in self.fields_internalizer.items():
            value = data.get(f'{field}')
            if not self.partial or value or value is not None:
                try:
                    internal_value[f'{field}'] = validator(value)
                except fieldError as e:
                    errors[f'{field}'] = e.msg
        if errors:
            raise serializers.ValidationError(errors)
        return internal_value

    def validate(self, attrs):
        errors = {}
        for field in self.fields_validation:
            filter_kwargs = {field: attrs.get(field)}
            if Pessoa.objects.filter(**filter_kwargs).exists():
                errors[field] = f"{attrs[f'{field}']} ja esta registrado em outra pessoa"
        try:        
            valida_conteudo_nucleos_particoes(attrs['nucleos'], attrs['particoes_especialidades'])
        except fieldError as e:
            errors['nucleos_e_particoes'] = e.msg


        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def to_representation(self, instance):
        '''
        Desserialização da instancia em objeto JSON
        '''
        fk_field = {
            f'{field}': self.fields_models[f'{field}'].objects.get(
                pessoa_id=instance.id
            )
            for field, serializer in self.fields_serializers.items()
        }
        # Trocar para mostrar as particoes_especialidades por nucleos
        nucleos_e_particoes = Particao_EspecialidadeSerializer().to_representation_por_pessoa(instance)

        return {
            'nome' : instance.nome,
            'nucleos_e_particoes': nucleos_e_particoes,
            'endereco': str(fk_field['endereco']),
            'classificacao' : instance.get_classificacao_display(),
            'telefone' : instance.telefone,
            'cpf_cnpj' : instance.cpf_cnpj,
            'data_nascimento' : instance.data_nascimento,
            'data_cadastro' : instance.data_cadastro
        }



    def create(self, validated_data):
        validated_data_nucleos = validated_data.pop('nucleos')
        validated_data_particoes_especialidades = validated_data.pop('particoes_especialidades')
        fk_validated_data = {
            key: validated_data.pop(f'{key}')
            for key in self.fields_serializers.keys()
        }
        pessoa = Pessoa.objects.create(**validated_data)
        for field, serializer in self.fields_serializers.items():
            if type(fk_validated_data[f'{field}']) == []: 
                for obj in fk_validated_data[f'{field}']:
                    print('pessoa',obj)
                    serializer().create(obj, pessoa)
                    continue
            dados = fk_validated_data[f'{field}']
            serializer().create(dados, pessoa)
        pessoa.nucleos.set(objs=validated_data_nucleos)
        pessoa.particoes_especialidades.set(objs=validated_data_particoes_especialidades)
        pessoa.save()
        return pessoa