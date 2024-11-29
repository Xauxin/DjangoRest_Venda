from typing import Dict, Type, Union
from django.db import models
from ..erros import *
from PIL import Image



def valida_dicionario_str_str(value, esquema=None):
    if esquema is None:
        esquema = []
    if not value:#caso não haja valor#
        raise fieldError(msg='O campo não pode ser nulo')
    if not isinstance(value, Dict):#caso o valor não seja no formato nescessário#
         raise fieldError(msg='O campo deve ser um dicionário com ids, ou nomes')
    chaves_invalidas = []
    valores_invalidos = []
    for chave, valor in value.items():
        if not isinstance(chave, str):
            chaves_invalidas.append(chave)
        if not isinstance(valor, str):
            valores_invalidos.append(valor)

    if chaves_invalidas or valores_invalidos:
        raise fieldError(msg=f'As seguintes chaves {chaves_invalidas}, e seguinte valores {valores_invalidos} são invalidos')
    return value





def valida_data(value, esquema=None):
    if esquema is None:
        esquema = []
    return value




def valida_string(string: Union[str, None], max_length: int, min_length: int, separador: str = "") -> str:
    if not string:
        raise fieldError(msg="O Campo não pode ser vazio ou nulo",value=string)
    if not isinstance(string, str):
        raise fieldError(msg="Os dados passados não estão em string",value=string)
    if not min_length <= len(string) <= max_length:
        raise fieldError(f"O limite de caracter é no máximo {max_length} e no mínimo {min_length}",value=string)
    if separador and separador not in string:
        raise fieldError(msg="O separador pedido não está ou esta sendo usado de forma incorreta",value=string)
    return string

def valida_float(value):
    if not value:
        raise fieldError(msg="O campo não pode ser vazio ou nulo",value=value)
    if not isinstance(value, (int, float)):
        raise fieldError(msg="Os dados passados não são um número",value=value)
    return value

def valida_chave_estrangeira(primary_keys:list[int] | int, model:Type[models.Model]):
    if not primary_keys:
        raise fieldError(msg="A lista não pode estar vazia",value=[])
    era_int = False
    if isinstance(primary_keys, int):
        era_int = True
        primary_keys = [primary_keys]
    if not isinstance(primary_keys, int|list):
        raise fieldError(msg="O valor deve ser um id de uma chave estrangeira", value=primary_keys)

    valid_primary_keys = []
    invalid_primary_keys = []
    for pk in primary_keys:
        try:
            instance = model.objects.get(id=pk)
            valid_primary_keys.append(instance)
        except model.DoesNotExist:
            invalid_primary_keys.append(pk)
    if invalid_primary_keys:
        raise fieldError(f"As seguintes primary keys são invalidas {invalid_primary_keys}", value=invalid_primary_keys)
    return valid_primary_keys[0] if era_int else valid_primary_keys

def valida_booleano(value):
    if not isinstance(value, bool):
        raise fieldError(msg="O valor deve ser Boolean. True ou False",value=value)
    return value

def valida_opcoes(value, option_tuples:set[tuple]):
    if not value:
        raise fieldError(msg="Este campo não pode ser nulo", value=value)
    if value not in dict(option_tuples):
        raise fieldError(f"A opção escolhida não é valida, essa são as opções {option_tuples}",value=value)
    return value

def valida_lista_de_dicionarios(lista, field:str, field_double_check:str=""):
    if not lista:
        raise fieldError(msg="Este campo não pode ser nulo nem vazio")
    if not isinstance(lista, list):
        raise fieldError(msg=f"Este campo deve ser uma lista de dicionário de {field}")
    duplicated_field = []
    if not_a_dict := [obj for obj in lista if not isinstance(obj, dict)]:
        raise fieldError(msg=f"Todos elementos dessa lista precisão ser um dicionário, esse são os que não são: {not_a_dict}")
    if field_double_check:
        value_of_fields = [obj[f'{field_double_check}'] for obj in lista]
        duplicated_field.extend(
            value
            for value in value_of_fields
            if (value_of_fields.count(value) > 1)
        )
    if duplicated_field:
        raise fieldError(msg=f"O campo {field_double_check}, não pode ter valores repetidos em um só dicionário, esse são os valores repetido {duplicated_field}")

    return lista

def valida_conteudo_nucleos_particoes(nucleos:models.QuerySet, particoes:models.QuerySet):
    if particoes_sem_nucleo := [
        particao.nome
        for particao in particoes
        if particao.nucleo not in nucleos
    ]:
        raise fieldError(msg=f"{particoes_sem_nucleo} não pertencem a nenhum nucleos escolhido")
        

def valida_imagem(imagem):
    if not imagem:
        raise fieldError(msg="Este Campo não pode ser nulo ou vazio")
    try:
        Image.open(imagem)
    except:
        raise fieldError(msg="Não é um caminho ou formato valido")
    return imagem




  