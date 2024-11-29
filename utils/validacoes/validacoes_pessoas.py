from dataclasses import field
from pickle import NONE
from socket import MsgFlag
from typing import Dict, Type, Union
from estoque.Suprimentos.Cores.cores_model import Cor
from venda.EsquemaProduto.esquema_produto_serializer import Medida, Suprimento, Tamanho, Modelagem
from venda.EsquemaProduto.Modelagem.OpcaoModelagem.opcao_modelagem_model import OpcaoModelagem
from django.db import models
from ..erros import *
from validate_docbr import CPF, CNPJ
import re, requests
from PIL import Image


def valida_endereco(value:dict[str,str]):
    if not isinstance(value, dict):
        raise fieldError(msg='O campo deve conter um dicionário com pelo menos o CEP e Numero ou Localidade e UF')
    chaves_cep_numero = {'cep', 'numero'}
    chaves_localidade_uf = {'localidade', 'uf'}
    if not (chaves_cep_numero.issubset(value.keys()) or chaves_localidade_uf.issubset(value.keys())):
        raise fieldError(msg='O campo deve conter um dicionário com pelo menos o CEP e Numero ou Localidade e UF')
    if 'cep' in value:
        modelo = r'([\d]{5})-?([\d]{3})'
        checagem = re.search(modelo, value['cep'])
        if not checagem:
            fieldError(msg='O formato do CEP não é aceito')
    if set(value.keys()) == {"cep", "numero"}:
        return complementa_endereco(value)
    return value

    
def complementa_endereco(endereco:dict) -> dict:
    cep = endereco['cep']
    via_cep = requests.get(f'https://viacep.com.br/ws/{cep}/json')
    via_cep_json = via_cep.json()
    campos_despresados = ['ibge', 'gia','unidade', 'siafi']
    for item in campos_despresados:
        if item in via_cep_json:
            via_cep_json.pop(item)  
    for key, value in via_cep_json.items():
        if key not in endereco:
            endereco[key] = value
    return endereco

def valida_telefone(tel:str):
    modelo = r"([(]?([0-9]{2})[)])?([0-9]{4,5})-?([0-9]{4})"
    checagem = re.search(modelo, tel)
    if not tel:
        raise fieldError(msg="O Campo nao pode ser vazio ou nulo")
    if not isinstance(tel, str):
        raise fieldError(msg="O Campo deve ser do tipo string")
    if not  8 <= len(tel) <= 17:
        raise fieldError(msg="O campo deve ter de de 8 a 17 caractéres")
    if not checagem:
        raise fieldError(msg="Esse formato não é aceito")
    return "".join(filter(str.isdigit, tel))
    
def valida_cpf_cnpj(cpf_cnpj):
    cpf = CPF()
    cnpj = CNPJ()

    # Remove qualquer caractere que não seja dígito
    documento = ''.join(filter(str.isdigit, cpf_cnpj))

    if len(documento) == 11:
        if not cpf.validate(documento):
            raise fieldError(msg='CPF inválido.')
        return cpf.mask(documento)
    if len(documento) == 14:
        # Se tiver 14 dígitos, valida como CNPJ
        if not cnpj.validate(documento):
            raise fieldError(msg='CNPJ inválido.')
        return cnpj.mask(documento)
    raise fieldError(msg='Número de CPF ou CNPJ inválido.')
