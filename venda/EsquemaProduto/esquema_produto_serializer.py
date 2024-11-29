from typing import Dict, Callable, Any
from utils.validacoes.validacoes_gerais import *
from rest_framework import serializers
from .Modelagem.modelagem_serializer import ModelagemSerializer, Modelagem
from .Tamanhos.tamanhos_serializer import TamanhoSerializer, Tamanho
from .Medidas.medidas_serializer import MedidaSerializer, Medida
from .esquema_produto_model import EsquemaProduto
from estoque.Suprimentos.suprimento_serializer import Suprimento, SuprimentoSerializer
from utils.erros import *

def internaliza_dados_de_outras_tabelas(data=None, serializer:serializers.Serializer=serializers.Serializer()):
    if data is None:
        data = []
    internal_value = []
    errors = {}

    for index, obj_data in enumerate(data):
        try:
            internal_value.append(serializer.to_internal_value(obj_data))
        except fieldError as e:
            errors[f'{index}'] = e.msg

    if errors:
        raise fieldError(errors)

    return internal_value


class EsquemaProdutoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=50)
    suprimentos = serializers.PrimaryKeyRelatedField(queryset=Suprimento.objects.all(), many=True)
    locais_de_bordado_sugeridos = serializers.CharField(max_length=50)
    valor_base = serializers.FloatField()

    field_validators = {
        'nome': lambda value: valida_string(value, 50, 1),
        'locais_de_bordado_sugeridos': lambda value: valida_string(value, 50, 1),
        'valor_base': lambda value: valida_float(value),
        'suprimentos': lambda value: valida_chave_estrangeira(value, Suprimento),
        'medidas': lambda value: valida_lista_de_dicionarios(value, 'medidas',field_double_check='nome'),
        'modelagens': lambda value: valida_lista_de_dicionarios(value, 'modelagens',field_double_check='nome'),
        'tamanhos': lambda value: valida_lista_de_dicionarios(value, 'tamanho',field_double_check='nome')
    }

    fields_serializers :Dict[str, type[MedidaSerializer]|type[TamanhoSerializer]|type[ModelagemSerializer]] = {
        'tamanhos':TamanhoSerializer,
        'medidas': MedidaSerializer,
        'modelagens':ModelagemSerializer,
    } 

    fields_models :Dict[str, type[Medida]|type[Tamanho]|Type[Modelagem]] = {
        'tamanhos':Tamanho,
        'medidas': Medida,
        'modelagens':Modelagem,
    } 

    def to_internal_value(self, data):
        """
        Converte os dados de entrada para um formato adequado para `create` e `update`.
        """
        errors = {}
        internal_value = {}

        for field, validator in self.field_validators.items():
            value = data.get(f'{field}')
            if not self.partial or value or value is not None:
                try:
                    internal = validator(value)
                    if field not in self.fields_serializers.keys():
                        internal_value[f'{field}'] = internal
                except fieldError as e:
                    errors[f'{field}'] = e.msg

        other_tables_internal_value = {}
        for field, serializer in self.fields_serializers.items():
            if field not in errors:
                value = data.get(f'{field}')
                if not self.partial or value or value is not None:
                    try:
                        internal = internaliza_dados_de_outras_tabelas(value , serializer())
                        other_tables_internal_value[field] = internal
                    except fieldError as e:
                        errors[f'{field}'] = e.msg  

        internal_value |= other_tables_internal_value

        if errors:
            raise serializers.ValidationError(errors)
        return internal_value

    def validate(self, attrs):
        if esquemas := EsquemaProduto.objects.filter(nome=attrs['nome']):
            raise serializers.ValidationError({"nome": "Esse nome ja existe ou é o nome do registro que tentou alterar"})
        return super().validate(attrs)


    def to_representation(self, instance):
        '''
        Desserialização da instancia em objeto JSON
        '''
        fk_field = {
            f'{field}': [
                serializer().to_representation(instancia)
                for instancia in self.fields_models[f'{field}'].objects.filter(
                    esquema_produto=instance.id
                )
            ]
            for field, serializer in self.fields_serializers.items()
        }
        suprimentos = [SuprimentoSerializer().to_representation(suprimento)
        for suprimento in instance.suprimentos.all()]
        return{
            "nome": instance.nome,
            'suprimentos': suprimentos,
            'modelagens': fk_field['modelagens'],
            'tamanhos': fk_field['tamanhos'],
            'medidas': fk_field['medidas'],
            "locais_de_bordado_sugeridos": instance.locais_de_bordado_sugeridos,
            "valor_base": instance.valor_base
        }

    def detailed_to_representation(self, instance):
        '''
        Desserialização detalhada da instancia em objeto JSON
        '''
        fk_field = {
            f'{field}': [
                serializer().detailed_to_representation(instancia)
                for instancia in self.fields_models[f'{field}'].objects.filter(
                    esquema_produto=instance.id
                )
            ]
            for field, serializer in self.fields_serializers.items()
        }
        suprimentos = [SuprimentoSerializer().detailed_to_representation(suprimento)
        for suprimento in instance.suprimentos.all()]
        return{
               "nome": instance.nome,
               'suprimentos': suprimentos,
               'modelagens': fk_field['modelagens'],
               'tamanhos': fk_field['tamanhos'],
               'medidas': fk_field['medidas'],
               "locais_de_bordado_sugeridos": instance.locais_de_bordado_sugeridos,
               "valor_base": instance.valor_base
        }
    def create(self, validated_data):
        '''
        Cria os objetos de Esquema_produto
        Juntamente cria todas as dependencias
        '''
        print(validated_data)
        validated_data_suprimento = validated_data.pop('suprimentos')
        fk_validated_data = {
            key: validated_data.pop(f'{key}')
            for key in self.fields_serializers.keys()
        }
        esquema_produto = EsquemaProduto.objects.create(**validated_data)
        for field, serializer in self.fields_serializers.items():
            for obj in fk_validated_data[f'{field}']:
                serializer().create(obj, esquema_produto)
        esquema_produto.suprimentos.set(objs=validated_data_suprimento)
        esquema_produto.save()
        return esquema_produto


    def update(self, instance, validated_data):
        for field in self.field_validators.keys():
            value = validated_data.get(field)
            if not self.partial or value or value is not None:    
                if field in self.get_fields().keys() and field != 'suprimentos':
                    setattr(instance, field, value)
                    instance.save()
                if field == 'suprimentos':
                    instance.suprimentos.set(value)
                    instance.save()
                if field in self.fields_serializers.keys():
                    self.fields_serializers[f'{field}']().update(instance=instance, validated_data=value)
        return instance


        



