from django.db import models
from pessoas.pessoas.pessoa_model import Pessoa
from .valores.valores_venda_model import ValoresVenda

class Venda(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.RESTRICT)
    status = models.CharField(max_length=50)
    valores = models.ForeignKey(ValoresVenda, on_delete=models.CASCADE)
    observacao = models.CharField(max_length=1000)
