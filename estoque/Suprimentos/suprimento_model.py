from django.db import models

class Suprimento(models.Model):
    UNIDADES_MEDIDAS = {
        ('m', 'Metro'),
        ('g', 'Grama'),
        ('Un', 'Unidade')
    }
    CLASSES = {
        ('T', 'Tecido'),
        ('L', 'Linha'),
        ('P', 'Peças'),
        ('A', 'Aviamentos')
    }
    nome = models.CharField(max_length=35)
    valor = models.FloatField()
    unidade_de_medida = models.CharField(max_length=2, choices=UNIDADES_MEDIDAS)
    classificacao = models.CharField(max_length=1,choices=CLASSES)
    cores = models.ManyToManyField('Cor', related_name='+')

    def __str__(self) -> str:
        return f'{self.nome}'

    def unidade_de_medida_str(self):
        return dict(self.UNIDADES_MEDIDAS)[self.unidade_de_medida]

    def classificacao_str(self):
        return dict(self.CLASSES)[self.classificacao]