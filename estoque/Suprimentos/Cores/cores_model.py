from django.db import models

class Cor(models.Model):
    nome = models.CharField(max_length=30, blank=False, null=False)
    cores_bordado = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nome