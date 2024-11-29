from django.db import models


class Nucleo(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    abreviado = models.CharField(max_length=4, blank=False, null=False)

    @classmethod
    def get_default_pk(cls):
        nucleo, created = cls.objects.get_or_create(
            id=1,
            defaults=dict(nome='Sem Nucleo'),
        )
        return nucleo.pk