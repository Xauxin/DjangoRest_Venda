from urllib.request import URLopener
from rest_framework import serializers
from .Imagem_Bordado_model import ImagemBordado, Bordado
from pessoas.nucleo.nucleo_model import Nucleo
from utils.validacoes.validacoes_gerais import * 
from typing import Dict
from utils.tools.redimensionar_imagem import redimensionar_imagem
from django.conf import settings



class ImagemBordadoSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def to_representation(self, instance):
        host = f'http://{settings.ALLOWED_HOSTS[0]}:8000'
        media_URL = settings.MEDIA_URL
        return{
            '60x': str(host + media_URL + str(instance.x60)),
            '120x': str(host + media_URL + str(instance.x120)),
            '240x': str(host + media_URL + str(instance.x240))
        }

    def create(self, validated_data, bordado_instance):
        imgs = redimensionar_imagem(validated_data, bordado_instance.codigo)
        return ImagemBordado.objects.create(**imgs, bordado = bordado_instance)
