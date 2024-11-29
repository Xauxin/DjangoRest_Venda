from django.db import models
from pessoas.nucleo.nucleo_model import Nucleo

class Particao_Especialidade(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    nucleo = models.ForeignKey(Nucleo, on_delete=models.CASCADE, null=False, blank=False, related_name='+')

    @classmethod
    def get_default_pk(cls):
        particao_especialidade, created = cls.objects.get_or_create(
            id=1,
            defaults=dict(nome='Sem Particao_Especialidade'),
        )
        return particao_especialidade.pk