from pessoas.Particao_Especialidade.particao_especialidade_model import Nucleo, Particao_Especialidade
from ..bordado.bordado_model import Bordado
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

class ImagemBordado(models.Model):
    imagem = models.CharField(max_length=300, blank=True, null=True)
    x60 = models.ImageField(blank=True, null=True)
    x120 = models.ImageField(blank=True, null=True)
    x240 = models.ImageField(blank=True, null=True)
    bordado = models.ForeignKey(Bordado, on_delete=models.CASCADE, related_name='+')



    def __str__(self) -> str:
        return f"Imagens do bordado: {self.bordado}"

@receiver(pre_delete, sender=ImagemBordado)
def delete_imagens(sender, instance, **kwargs):
    fields = [instance.x60, instance.x120, instance.x240]
    for imagem in fields:
        if imagem:
            os.remove(imagem.path)