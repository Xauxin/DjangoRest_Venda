from django.db import models
from ..produto_model import Produto
from bordados.bordado.bordado_model import Bordado


class Bordado_Produto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT)
    bordado = models.ForeignKey(Bordado, on_delete=models.RESTRICT)
    local = models.CharField(max_length=50)