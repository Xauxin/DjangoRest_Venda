from dataclasses import field
from pickle import NONE
from socket import MsgFlag
from traceback import print_tb
from turtle import mode
from typing import Dict, Type, Union
from estoque.Suprimentos.Cores.cores_model import Cor
from venda.EsquemaProduto.esquema_produto_serializer import Medida, Suprimento, Tamanho, Modelagem
from venda.EsquemaProduto.Modelagem.OpcaoModelagem.opcao_modelagem_model import OpcaoModelagem
from django.db import models
from ..erros import *
from validate_docbr import CPF, CNPJ
import re, requests
from PIL import Image

def valida_nome_com_esquema(value,esquema):
    if esquema.nome != value:
        raise fieldError(msg='O nome passado não é o mesmo do Esquema passado')
    return value


def valida_tecido_com_esquema(value,esquema):
    tecido = esquema.suprimentos.filter(id = value['tecido_id'])
    if not tecido:
        raise fieldError(msg='O tecido escolhido não pertence ao Esquema escolhido')
    if cor := tecido[0].cores.filter(id=value['cor_id']):
        return value
    else:
        raise fieldError(msg='O tecido escolhido não contem essa cor')


def valida_tamanho_com_esquema(value,esquema):
    tamanho = Tamanho.objects.get(id = value['tamanho_id'])
    if tamanho.esquema_produto != esquema:
        raise fieldError(msg='Esse tamanho não pertence ao Esquema escolhido')
    return value

def valida_modelagem_com_esquema(data,esquema):
    modelagens = pega_modelagem_e_opcoes(esquema)
    erros = {}
    requeridos = []
    for key, value in modelagens.items():
        requerido = value['requerido']
        if requerido:
            requeridos.append(key)
    if campos_requeridos_fora_da_data := [
        requerido for requerido in requeridos if requerido not in data.keys()
    ]:
        erros['Requerido'] = f'Os campos {campos_requeridos_fora_da_data} são obrigatórios'
    for key, value in data.items():
        if key not in modelagens.keys():
            erros[key] = 'Essa modelagem não pertence ao Esquema escolhido'
            continue
        if value not in modelagens[key]['opcoes']:
            erros[key] = f'{value} não existe na Modelagem escolhida'

    if erros:
        raise fieldError(msg=erros)

    return data
    


def valida_medidas_com_esquema(data,esquema):
    erros = {}
    medidas = pega_medidas(esquema)
    if campos_requeridos_fora_da_data := [
        requerido
        for requerido in medidas['requeridas']
        if requerido not in data.keys()
    ]:
        erros['Requerido'] = f'Os campos {campos_requeridos_fora_da_data} são obrigatórios'
    for key, value in data.items():
        if key not in medidas['requeridas'] and key not in medidas['outras']:
            erros[key] = 'Essa Medida nao pertence ao Esquema escolhido'

    if erros:
        raise fieldError(msg=erros)

    return data

def valida_tecido(value):
    """
    Valida um valor de tecido fornecido.

    Args:
        value (dict): Um dicionário contendo informações do tecido, incluindo id ou nome, e informações da cor, incluindo id ou nome.

    Returns:
        dict: O valor de tecido validado, ou o resultado de internaliza_dados se tecido_id estiver presente.

    Raises:
        fieldError: Se o valor for nulo, não for um dicionário ou estiver faltando campos obrigatórios.
        fieldError: Se o tecido_id ou cor_id não for encontrado.
        fieldError: Se o tecido_nome ou cor_nome não for uma string.
    """
    if not value:#caso não haja valor#
        raise fieldError(msg='O campo não pode ser nulo')
    if not isinstance(value, Dict):#caso o valor não seja no formato nescessário#
         raise fieldError(msg='O campo deve ser um dicionário com ids, ou nomes')
    if 'tecido_id' not in value and 'tecido_nome' not in value:
        print('aqui')
        raise fieldError(msg="Nome ou id do tecido são nescessários")
    if 'cor_id' not in value and 'cor_nome' not in value:
        raise fieldError(msg="Nome ou id da cor são nescessários")
    if 'tecido_id' in value:
        try:
            return internaliza_dados(value)
        except Suprimento.DoesNotExist as e:
            raise fieldError(msg='O id passado não existe') from e
    if 'tecido_nome' in value:
        if 'cor_id' in value:
            raise fieldError(msg='Caso o tecido seja referenciado pelo nome, não se deve passar cor_id')
        if not isinstance(value['tecido_nome'], str):
            raise fieldError(msg='Ao referenciar o tecido pelo nome, o mesmo deve ser uma string')
        if not isinstance(value['cor_nome'], str):
            raise fieldError(msg='Ao referenciar a cor pelo nome, a mesma deve ser uma string')
        return value


# TODO Rename this here and in `valida_tecido`
def internaliza_dados(value):
    tecido = Suprimento.objects.get(id = value['tecido_id'])
    if tecido.classificacao != "T": #caso o id passado não seja um tecido#
        raise fieldError(msg='O id do suprimento passado não é um tecido')
    if 'tecido_nome' in value and value['tecido_nome'] != tecido.nome:#caso o nome do tecido passado seja diferente do nome do id passado#
        raise fieldError(msg='Caso for passado id e nome os dois devem referir ao mesmo Tecido')
    if 'cor_id' not in value:
        raise fieldError(msg="Com foi passado tecido_id, cor_id também é nescessário")
    cores = tecido.cores.all().values_list('id', flat=True)
    if value['cor_id'] not in cores:#caso não haja a cor no tecido passado#
        raise fieldError(msg='Não existe essa cor para esse Tecido')
    if 'cor_nome' in value and value['cor_nome'] != tecido.cores.get(id = value['cor_id']).nome:#caso o nome da cor passado seja diferente do nome do id passado#
        raise fieldError(msg='Caso for passado id e nome os dois devem referir a mesma Cor')
    return value

def valida_tamanho(value):
    if not value:#caso não haja valor#
        raise fieldError(msg='O campo não pode ser nulo')
    if not isinstance(value, Dict):#caso o valor não seja no formato nescessário#
         raise fieldError(msg='O campo deve ser um dicionário com ids, ou nomes')
    if 'tamanho_id' not in value and 'tamanho_nome' not in value:
        raise fieldError(msg='Nome ou id do tamanho são nescessários')
    if 'tamanho_id' in value:
        try:
            tamanho = Tamanho.objects.get(id = value['tamanho_id'])
            if 'tamanho_nome' in value and value['tamanho_nome'] != tamanho.nome:
                raise fieldError(msg='Caso for passado id e nome os dois devem referir ao mesmo Tamanho')
        except Tamanho.DoesNotExist as e:
            raise fieldError(msg='O id passado não existe') from e
    return value


def valida_esquema_ou_nome(value, nome):
    if not value and not nome:
        raise fieldError(msg='')


def pega_modelagem_e_opcoes(esquema):
    modelagens_e_opcoes = {}
    modelagems = Modelagem.objects.filter(esquema_produto = esquema.pk)
    for modelagem in modelagems:
        modelagens_e_opcoes[f'{modelagem.nome}'] = {'requerido': modelagem.requerido, 'opcoes': []}
        opcoes = OpcaoModelagem.objects.filter(modelagem = modelagem.pk)
        for opcao in opcoes:
            modelagens_e_opcoes[modelagem.nome]['opcoes'].append(opcao.nome)
   
    return modelagens_e_opcoes

def pega_medidas(esquema):
    medidas = {'requeridas': [], 'outras':[]}
    medidas_do_esquema = Medida.objects.filter(esquema_produto = esquema.pk)
    for medida in medidas_do_esquema:
        if medida.validacoes == "O":
            medidas['requeridas'].append(medida.nome)
        else:
            medidas['outras'].append(medida.nome)
    return medidas