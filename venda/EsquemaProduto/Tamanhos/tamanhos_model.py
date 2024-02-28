from django.db import models

class Tamanho(models.Model):
    COMPLEXIDADES = {
        (1, 'Facil'),
        (2, 'Normal'),
        (3, 'Avançado'),
        (4, 'Difícil'),
        (5, 'Muito Difícil')
    }

    nome = models.CharField(max_length=3)
    complexidade = models.IntegerField(choices=COMPLEXIDADES, null=False, blank=False)
    esquema_produto = models.ForeignKey('EsquemaProduto', on_delete=models.CASCADE, null=False, blank=False, related_name='+')


    def __str__(self) -> str:
        return self.nome
    
    def complexidade_str(self, nota_de_complexidade):
        return dict(self.COMPLEXIDADES)[nota_de_complexidade]