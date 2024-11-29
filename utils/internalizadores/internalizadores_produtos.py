from dataclasses import field
from distutils.log import error
from pickle import NONE
from socket import MsgFlag
from typing import Dict, Type, Union
from .internalizadores_gerais import *
from estoque.Suprimentos.Cores.cores_model import Cor
from venda.EsquemaProduto.esquema_produto_serializer import Medida, Suprimento, Tamanho, Modelagem
from venda.EsquemaProduto.Modelagem.OpcaoModelagem.opcao_modelagem_model import OpcaoModelagem
from django.db import models
from ..erros import *
from validate_docbr import CPF, CNPJ
import re, requests
from PIL import Image

def internaliza_tecido_com_esquema(value):
    if not value:#caso não haja valor#
        raise fieldError(msg='O campo não pode ser nulo')
    if not isinstance(value, Dict):#caso o valor não seja no formato nescessário#
         raise fieldError(msg='O campo deve ser um dicionário com id de tecido e cor')
    if 'tecido_id' not in value or 'cor_id' not in value:
        raise fieldError(msg="No caso de produtos com esquema é nescesssário usar id como referencia de tecido e cor")
    try:
        return internaliza_dados(value)
    except Suprimento.DoesNotExist as e:
        raise fieldError(msg='O id passado não existe') from e


def internaliza_dados(value):
    tecido = Suprimento.objects.get(id = value['tecido_id'])
    cores = tecido.cores.all().values_list('id', flat=True)
    if tecido.classificacao != "T": #caso o id passado não seja um tecido#
        raise fieldError(msg='O id do suprimento passado não é um tecido')
    if 'tecido_nome' in value and value['tecido_nome'] != tecido.nome:#caso o nome do tecido passado seja diferente do nome do id passado#
        raise fieldError(msg='Caso for passado id e nome os dois devem referir ao mesmo Tecido')
    if 'tecido_nome' not in value:
        value['tecido_nome'] = tecido.nome
    if value['cor_id'] not in cores:#caso não haja a cor no tecido passado#
        raise fieldError(msg='Não existe essa cor para esse Tecido')
    if 'cor_nome' in value and value['cor_nome'] != tecido.cores.get(id = value['cor_id']).nome:#caso o nome da cor passado seja diferente do nome do id passado#
        raise fieldError(msg='Caso for passado id e nome os dois devem referir a mesma Cor')
    if 'cor_nome' not in value:
        value['cor_nome'] = tecido.cores.get(id = value['cor_id']).nome
    return value
    
        

def internaliza_tamanho_com_esquema(value):
    if not value:#caso não haja valor#
        raise fieldError(msg='O campo não pode ser nulo')
    if not isinstance(value, Dict):#caso o valor não seja no formato nescessário#
         raise fieldError(msg='O campo deve ser um dicionário com ids')
    if 'tamanho_id' not in value:
        raise fieldError(msg='No caso de produtos com esquema é nescesssário usar id como referencia de tamanho')
    try:
        tamanho = Tamanho.objects.get(id = value['tamanho_id'])
        if 'tamanho_nome' in value and value['tamanho_nome'] != tamanho.nome:
            raise fieldError(msg='Caso for passado id e nome os dois devem referir ao mesmo Tamanho')
        if 'tamanho_nome' not in value:
            value['tamanho_nome'] = tamanho.nome
    except Tamanho.DoesNotExist as e:
        raise fieldError(msg='O id passado não existe') from e
    return value

def internaliza_tecido_sem_esquema(value):
    errors = {}
    if not value:#caso não haja valor#
        raise fieldError(msg='O campo não pode ser nulo')
    if not isinstance(value, Dict):#caso o valor não seja no formato nescessário#
         raise fieldError(msg='O campo deve ser um dicionário com id de tecido e cor')
    if 'tecido_nome' not in value or 'cor_nome' not in value:
        raise fieldError(msg="No caso de produtos sem esquema deve sómente referenciar com nomes de tecido e cor")
    if 'tecido_id' in value or 'cor_id' in value:
        raise fieldError(msg="No caso de produtos sem esquema deve sómente referenciar com nomes")
    try:
        value['tecido_nome'] = internaliza_string(value['tecido_nome'], 50,4)
    except fieldError as e:
        errors['tecido'] = e.msg
    try:
        value['cor_nome'] = internaliza_string(value['cor_nome'], 50, 3)
    except fieldError as e:
        errors['cor'] = e.msg
    if errors:
        raise fieldError(msg=errors)
    return value

    
    
        

def internaliza_tamanho_sem_esquema(value):
    if not value:#caso não haja valor#
        raise fieldError(msg='O campo não pode ser nulo')
    if not isinstance(value, Dict):#caso o valor não seja no formato nescessário#
         raise fieldError(msg='O campo deve ser um dicionário com nome')
    if 'tamanho_id' in value or 'tamanho_nome' not in value:
        raise fieldError(msg='No caso de produtos sem esquema é nescesssário usar sómente o nome como referencia de tamanho')
    value['tamanho_nome'] = internaliza_string(value['tamanho_nome'], 50,2)
    return value

def internaliza_taxas_e_desconto(data):
    erros = {}
    if not data:
        raise fieldError(msg='Esse campo é obrigatório')
    if not isinstance(data, dict):
        raise fieldError(msg='Esse campo deve ser um dicionário de tipo(str) e valor(float)')
    tipos = ['porcentagem', 'fixo']
    campos = {'tipo':type(str), 'valor':type(float)}
    for campo, value in data.items():
        if campo not in campos.keys():
            erros[campo] = 'Essa chave não faz parte dos campos desse campo'
            continue
        if campo == 'tipo' and  value not in tipos:
            erros[campo] = f'{value} não é um tipo valido, validos:{tipos}'
            continue
        if campo == 'valor' and not isinstance(value, (float, int)):
            erros[campo] = 'O valor deve ser um Float ou Int'

    if erros:
        raise fieldError(msg=erros)

    return data

def internaliza_frete(data):
    erros = {}
    if not data:
        raise fieldError(msg='Esse campo é obrigatório')
    if not isinstance(data, dict):
        raise fieldError(msg='Esse campo deve ser um dicionário de tipo(str) e valor(float)')
    tipos = ['correios', 'particular']
    campos = {'tipo':type(str), 'valor':type(float)}
    for campo, value in data.items():
        if campo not in campos.keys():
            erros[campo] = 'Essa chave não faz parte dos campos desse campo'
            continue
        if campo == 'tipo' and  value not in tipos:
            erros[campo] = f'{value} não é um tipo valido, validos:{tipos}'
            continue
        if campo == 'valor' and not isinstance(value, (float, int)):
            erros[campo] = 'O valor deve ser um Float ou Int'

    if erros:
        raise fieldError(msg=erros)

    return data