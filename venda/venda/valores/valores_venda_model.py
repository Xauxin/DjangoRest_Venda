from django.db import models


class ValoresVenda(models.Model):
    produtos = models.FloatField()
    taxas = models.JSONField()
    frete = models.JSONField()
    desconto = models.JSONField()
    total = models.FloatField()
