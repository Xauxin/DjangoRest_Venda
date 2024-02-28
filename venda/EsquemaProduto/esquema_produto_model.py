from django.db import models
from estoque.Suprimentos.suprimento_model import Suprimento

class EsquemaProduto(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    suprimento = models.ManyToManyField(Suprimento, related_name='+')
    locais_de_bordado_sugeridos = models.CharField(max_length = 50)
    valor_base = models.FloatField( blank=False, null=False)