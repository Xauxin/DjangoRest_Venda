from ast import Try
from typing import Dict, Callable, Any
from utils.internalizadores.internalizadores_gerais import *
from rest_framework import serializers
from estoque.Suprimentos.suprimento_serializer import Suprimento, SuprimentoSerializer
from utils.erros import *
from venda.venda.valores.valores_venda_model import ValoresVenda
from venda.venda.valores.valores_venda_serializer import Valores_venda_Serializer
from .venda_model import Venda, Pessoa
from .produtos.produto_serializer import ProdutoSerializer, Produto


def valida_dados_de_outras_tabelas(attrs=None, serializer=None, many=False, valor_dos_produtos=None):
    """
    Valida dados de outras tabelas.

    Args:
        attrs (list, optional): Uma lista de atributos a serem validados. Padrão é None.
        serializer (Serializer, optional): Uma instância de serializador para validar os dados. Padrão é None.
        many (bool, optional): Se deve validar múltiplos objetos. Padrão é False.
        valor_dos_produtos (list, optional): Uma lista de valores dos produtos. Padrão é None.

    Returns:
        list: Uma lista de dados validados.

    Raises:
        ValueError: Se o serializador for None.
        fieldError: Se a validação falhar.
    """
    if attrs is None:
        attrs = []
    if serializer is None:
        raise ValueError("Serializer não pode ser None")
    if valor_dos_produtos is None:
        valor_dos_produtos = 0
    internal_value = []
    errors = {}
    if many:
        for index, obj_attrs in enumerate(attrs):
            try:
                internal_value.append(serializer(data=obj_attrs).validate(obj_attrs))
            except fieldError as e:
                errors[f'{index}'] = e.msg
    elif valor_dos_produtos:
        try:
            internal_value = serializer().validate(attrs, valor_dos_produtos)
        except fieldError as e:
            errors = e.msg
    else:
        try:
            internal_value = serializer().validate(attrs)
        except fieldError as e:
            errors = e.msg

    if errors:
        raise fieldError(errors)
    return internal_value


def internaliza_dados_de_outras_tabelas(data=None, serializer=None, many=False):
    if data is None:
        data = []
    if serializer is None:
        raise ValueError("Serializer não pode ser None")
    internal_value = []
    errors = {}
    if many:
        for index, obj_data in enumerate(data):
            try:
                internal_value.append(serializer(
                    data=obj_data).to_internal_value(obj_data))
            except fieldError as e:
                errors[f'{index}'] = e.msg
    else:
        try:
            internal_value = serializer().to_internal_value(data)
        except fieldError as e:
            errors = e.msg

    if errors:
        raise fieldError(errors)

    return internal_value


class VendaSerializer(serializers.Serializer):

    field_validators = {
        'pessoa': lambda value: internaliza_chave_estrangeira(value, Pessoa),
        'status': lambda value: internaliza_string(value, 50, 1),
        'valores': lambda value: internaliza_valores_venda(value),
        'observacao': lambda value: internaliza_string(value, 1000, 0),
        'produtos': lambda value: internaliza_lista_de_dicionarios(value, 'produtos')
    }

    fields_serializers = {
        'produtos': ProdutoSerializer,
        'valores': Valores_venda_Serializer
    }

    fields_models = {
        'produtos': Produto,
        'valores': ValoresVenda
    }

    def to_internal_value(self, data):
        """
        Converte os dados de entrada para um formato adequado para `create` e `update`.
        """
        internal_value = {}
        errors = {}
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
                        if field == 'produtos':
                            internal = internaliza_dados_de_outras_tabelas(
                                value, serializer, many=True)
                        else:
                            internal = internaliza_dados_de_outras_tabelas(
                                value, serializer)
                        other_tables_internal_value[field] = internal
                    except fieldError as e:
                        errors[f'{field}'] = e.msg

        internal_value |= other_tables_internal_value
        if errors:
            
            raise serializers.ValidationError(errors)

        return internal_value

    def validate(self, attrs):
        validated_data = attrs
        other_tables_validated_data = {}
        erros = {}
        valor_dos_produtos = 0
        for field, serializer in self.fields_serializers.items():
            if field not in erros:
                value = attrs.get(f'{field}')
                if not self.partial or value or value is not None:
                    try:
                        if field == 'produtos':
                            validator = valida_dados_de_outras_tabelas(value, serializer, many=True)
                            for produto in validator:
                                valor_dos_produtos += produto['valor']
                        elif field == 'valores':
                            if 'produtos' in erros:
                                continue
                            validator = valida_dados_de_outras_tabelas(value, serializer, valor_dos_produtos=valor_dos_produtos)
                        else:
                            validator = valida_dados_de_outras_tabelas(value, serializer)
                        other_tables_validated_data[field] = validator
                    except fieldError as e:
                        erros[f'{field}'] = e.msg

        validated_data.update(other_tables_validated_data)
        if erros:
            raise serializers.ValidationError(erros)

        return validated_data


    def to_representation(self, instance):
        '''
        Desserialização da instancia em objeto JSON
        '''
        produtos_venda = Produto.objects.filter(venda_id=instance.pk)
        produtos = [
            ProdutoSerializer(data="").to_representation(produto)
            for produto in produtos_venda
        ]
        pessoa = Pessoa.objects.get(id=instance.pessoa.pk)
        valores = Valores_venda_Serializer().to_representation(
            ValoresVenda.objects.get(id=instance.valores.pk))

        return {
            'pessoa': pessoa.nome,
            'status': instance.status,
            'produtos': produtos,
            'valores': valores
        }


    def detailed_to_representation(self, instance):
        '''
        Desserialização detalhada da instancia em objeto JSON

        Retorna a representacao detalhada da instancia em um dicionario
        com as seguintes chaves:
            - pessoa: nome da pessoa
            - status: status da venda
            - produtos: lista de dicionarios com os detalhes de cada produto
            - valores: dicionario com os valores da venda
        '''
        produtos_venda = Produto.objects.filter(venda_id=instance.pk)
        produtos = [
            ProdutoSerializer(data="").detailed_to_representation(produto)
            for produto in produtos_venda
        ]
        pessoa = Pessoa.objects.get(id=instance.pessoa.pk)
        valores = Valores_venda_Serializer().to_representation(
            ValoresVenda.objects.get(id=instance.valores.pk)
        )

        return {
            'pessoa': pessoa.nome,
            'status': instance.status,
            'produtos': produtos,
            'valores': valores
        }


    def create(self, validated_data):
        '''
        Cria os objetos de Venda
        Juntamente cria todas as dependencias
        '''
        fk_vali dated_data = {
            key: validated_data.pop(f'{key}')
            for key in self.fields_serializers.keys()
        }
        data_valores = fk_validated_data['valores']
        valores = ValoresVenda.objects.create(**data_valores)
        venda = Venda.objects.create(**validated_data, valores=valores)
        for field, serializer in self.fields_serializers.items():
            if field == 'valores':
                continue
            if field == 'produtos':
                for obj in fk_validated_data[f'{field}']:
                    serializer(data=obj).create(obj, venda)
        venda.save()
        return venda


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
                    self.fields_serializers[f'{field}']().update(
                        instance=instance, validated_data=value)
        return instance
