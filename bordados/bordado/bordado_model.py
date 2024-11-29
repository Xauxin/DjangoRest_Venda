from pessoas.Particao_Especialidade.particao_especialidade_model import Nucleo, Particao_Especialidade
from django.db import models




class Bordado(models.Model):
    ESTILOS = {
        ('B1', 'Brasão'),
        ('B2', 'Logo'),
        ('B3', 'Escrita'),
        ('B4', 'Outros')
    }

    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    estilo = models.CharField(max_length=2, choices=ESTILOS, default='B4')
    nucleo = models.ForeignKey(Nucleo, on_delete=models.SET_DEFAULT, default=Nucleo.get_default_pk)
    particao_especialidade = models.ForeignKey(Particao_Especialidade, on_delete=models.SET_DEFAULT, default=Particao_Especialidade.get_default_pk)
    valor = models.FloatField()

    def __str__(self) -> str:
        return f"({self.codigo})-{self.nome}"

    def get_estilo(self):
        return dict(self.ESTILOS)[self.estilo]



