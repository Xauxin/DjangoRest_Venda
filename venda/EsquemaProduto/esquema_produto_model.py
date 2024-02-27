from django.db import models

class EsquemaProduto(models.Model):
    nome = models.CharField(max_length=50, blanck=False, null=False)
    valor_base = models.FloatField( blanck=False, null=False)