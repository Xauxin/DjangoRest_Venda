from django.db import models

class Modelagem(models.Model):
    TIPOS = [
        ('U', 'Unico'),
        ('V', 'Varias Escolhas')
    ]

    nome = models.CharField(max_length=50, blank=False, null=False)
    requerido = models.BooleanField()
    tipo = models.CharField(max_length= 1, choices=TIPOS)
    esquema_produto = models.ForeignKey('EsquemaProduto', on_delete=models.CASCADE, null=False, blank=False, related_name='+')

    def tipo_str(self, tipo):
        return dict(self.TIPOS)[tipo]