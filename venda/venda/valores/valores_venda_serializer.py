from ast import Try
from typing import Dict, Callable, Any
from utils.validacoes.validacoes_gerais import *
from rest_framework import serializers
from estoque.Suprimentos.suprimento_serializer import Suprimento, SuprimentoSerializer
from utils.erros import *
from utils.internalizadores.internalizadores_produtos import *
from utils.internalizadores.internalizadores_gerais import *




class Valores_venda_Serializer(serializers.Serializer):

    field_validators = {
    'produtos':lambda value:  internaliza_float(value),
    'taxas':lambda value:  internaliza_taxas_e_desconto(value),
    'frete':lambda value:  internaliza_frete(value),
    'desconto':lambda value: internaliza_taxas_e_desconto(value),
    'total':lambda value:  internaliza_float(value)
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
                    internal_value[f'{field}'] = validator(value)
                except fieldError as e:
                    errors[f'{field}'] = e.msg
        print(internal_value)
        if errors:
            raise fieldError(errors)
        return internal_value

    def calcula_taxas(self, taxas, produtos):
        if 'valor' not in taxas:
            taxas['valor'] = 0
        if taxas['tipo'] == 'porcentagem':
            return produtos * (taxas['valor'] / 100)
        else:
            return taxas['valor']
        
    def calcula_descontos(self, desconto, produtos):
        if 'valor' not in desconto:
            desconto['valor'] = 0
        if desconto['tipo'] == 'porcentagem':
            return produtos * (desconto['valor'] / 100)
        else:
            return desconto['valor']


    def validate(self, attrs, valor_dos_produtos):
        erros = {}
        if attrs['produtos'] != valor_dos_produtos:
            erros['Cruzamento de informação'] = 'O valor de produtos em valores, difere da soma de todos produtos passados'
        #fazendo contas
        total_descontos = self.calcula_descontos(attrs['desconto'], attrs['produtos'])
        total_taxas = self.calcula_taxas(attrs['taxas'], attrs['produtos'])
        conta = round(attrs['produtos'] + total_taxas + attrs['frete']['valor'] - total_descontos, 2)
        print(conta)    
        if attrs['total'] != conta:
            erros['Cruzamento de informação'] = 'O valor total em valores, difere da soma de todos produtos, taxas e descontos passados'
        if erros:
            raise fieldError(msg=erros)
        return attrs

    def to_representation(self, instance):
        return {
        'produtos':instance.produtos,
        'taxas':instance.taxas,
        'frete':instance.frete,
        'desconto':instance.desconto,
        'total':instance.total
        }

    
