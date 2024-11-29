from django.db import models
from pessoas.nucleo.nucleo_model import Nucleo
from ..Particao_Especialidade.particao_especialidade_model import Particao_Especialidade


class Pessoa(models.Model):
    CLASSIFICACOES = {
        ('C', "Cliente"),
        ('P', "Prestador de Serviço"),
        ('F', "Funcionário"),
        ('E', "Empresa")
    }

    nome = models.CharField(max_length=50, blank=False, null=False)
    nomes_bordado = models.JSONField(blank=True, null=True)
    nucleos = models.ManyToManyField(Nucleo, blank=True, related_name='+')
    particoes_especialidades = models.ManyToManyField(Particao_Especialidade, blank=True, related_name='+')
    classificacao = models.CharField(max_length= 1, choices=CLASSIFICACOES)
    telefone = models.CharField(max_length=13, blank=False, null=False)
    cpf_cnpj = models.CharField(max_length=14, blank=False, null=False, db_index=True)
    data_nascimento = models.DateField( blank=False, null=False)
    data_cadastro = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=13, blank=False, null=False)

    def classificacao_str(self, classificacao):
        return dict(self.CLASSIFICACOES)[classificacao]