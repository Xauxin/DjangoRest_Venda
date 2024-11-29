from django.db import models

from pessoas.pessoas.pessoa_model import Pessoa

class Endereco(models.Model):
    cep = models.CharField(max_length=9, blank=True, null=True)
    logradouro = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento= models.CharField(max_length=100, blank=True, null=True)
    bairro= models.CharField(max_length=50, blank=True, null=True)
    localidade= models.CharField(max_length=50, blank=True, null=True)
    uf= models.CharField(max_length=3, blank=True, null=True)
    ddd= models.CharField(max_length=100, blank=True, null=True)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, null=False, blank=False, related_name='+')

    def __str__(self):
        if self.cep:
            return f"{self.logradouro}, {self.numero} - {self.bairro} - {self.localidade}, {self.uf}"
        return f"{self.localidade}, {self.uf}"