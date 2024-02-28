from django.db import models

class OpcaoModelagem(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    valor= models.FloatField()
    modelagem = models.ForeignKey('Modelagem', on_delete=models.CASCADE, null=False, blank=False, related_name='+')