from venda.EsquemaProduto.Modelagem.OpcaoModelagem.opcao_modelagem_model import OpcaoModelagem
from ..EsquemaProduto.esquema_produto_serializer import *
from estoque.Suprimentos.Cores.cores_model import Cor 

def create_cor(nome, cores_bordado, hex_value):
    return Cor.objects.create(
        nome=nome,
        cores_bordado=cores_bordado,
        hex=hex_value
    )

def create_suprimento(nome, valor, unidade_de_medida, classificacao):
    return Suprimento.objects.create(
        nome=nome,
        valor=valor,
        unidade_de_medida=unidade_de_medida,
        classificacao=classificacao
    )

def create_esquema_produto(nome, locais_de_bordado_sugeridos, valor_base):
    return EsquemaProduto.objects.create(
        nome=nome,
        locais_de_bordado_sugeridos=locais_de_bordado_sugeridos,
        valor_base=valor_base
    )

def create_medida(nome, validacoes, primeira_pagina, complexidade, esquema_produto):
    return Medida.objects.create(
        nome=nome,
        validacoes=validacoes,
        primeira_pagina=primeira_pagina,
        complexidade=complexidade,
        esquema_produto=esquema_produto
    )

def create_modelagem(nome, requerido, tipo, esquema_produto):
    return Modelagem.objects.create(
        nome=nome,
        requerido=requerido,
        tipo=tipo,
        esquema_produto=esquema_produto
    )

def create_opcao_modelagem(nome, valor, modelagem):
    return OpcaoModelagem.objects.create(
        nome=nome,
        valor=valor,
        modelagem=modelagem
    )

def create_tamanho(nome, complexidade, esquema_produto):
    return Tamanho.objects.create(
        nome=nome,
        complexidade=complexidade,
        esquema_produto=esquema_produto
    )
