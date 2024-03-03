from django.db import models
from ..esquema_produto_model import EsquemaProduto

class Medida(models.Model):
    VALIDACOES = {
        ('O', 'Opicional'),
        ('A', 'Aviso'),
        ('R', 'Requerido')
    }
    COMPLEXIDADES = {
        (1, 'Facil'),
        (2, 'Normal'),
        (3, 'Avançado'),
        (4, 'Difícil'),
        (5, 'Muito Difícil')
    }


    nome = models.CharField(max_length=50, blank=False, null=False)
    validacoes = models.CharField(max_length= 1, choices=VALIDACOES)
    primeira_pagina = models.BooleanField()
    complexidade = models.IntegerField(choices=COMPLEXIDADES, null=False, blank=False)
    esquema_produto = models.ForeignKey(EsquemaProduto, on_delete=models.CASCADE, null=False, blank=False, related_name='+')

    def complexidade_str(self, nota_de_complexidade):
        return dict(self.COMPLEXIDADES)[nota_de_complexidade]


