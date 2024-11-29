from django.db import models

from venda.EsquemaProduto.Tamanhos.tamanhos_model import Tamanho
from ..venda_model import Venda
from ...EsquemaProduto.esquema_produto_model import EsquemaProduto, Suprimento
from estoque.Suprimentos.Cores.cores_model import Cor


class Produto(models.Model):
    
    CLASSES = {
        ("c/E", "Com Esquema"),
        ("s/E", "Sem Esquema")
    }


    venda = models.ForeignKey(Venda, on_delete=models.RESTRICT)
    esquema = models.ForeignKey(EsquemaProduto, on_delete=models.RESTRICT, blank=True, null=True, related_name='+')
    nome = models.CharField(max_length=50, blank=False, null=False)
    tipo = models.CharField(max_length=3, choices=CLASSES)
    tecido = models.JSONField()
    tamanho = models.JSONField()
    modelagem = models.JSONField()
    medidas = models.JSONField()
    valor = models.FloatField()
    observacoes = models.CharField(max_length=1000)

    # tecido = {
    #   tecido_id = int
    #   tecido_nome = string
    #   cor_id = int
    #   cor_nome = string
    # }

    #  tamanho= {
    #   tamanho_id = int
    #   tamanho_nome = string
    # }

    # medidas = {
    #   medida1= medida1value
    #   medida2= medida2value
    #   medida3= medida3value
    # }

    # modelagem = {
    #   modelagem1= modelagem1value
    #   modelagem2= modelagem2value
    #   modelagem3= medida3value
    # }

    