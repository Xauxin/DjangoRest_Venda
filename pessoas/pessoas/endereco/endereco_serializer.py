from rest_framework import serializers
from .endereco_model import Endereco
from utils.validacoes.validacoes_gerais import *


class EnderecoSerializer(serializers.Serializer):
    cep = serializers.CharField(max_length=9)
    logradouro = serializers.CharField(max_length=100)
    numero = serializers.CharField(max_length=20)
    complemento= serializers.CharField(max_length=100)
    bairro= serializers.CharField(max_length=50)
    localidade= serializers.CharField(max_length=50)
    uf= serializers.CharField(max_length=3)
    ddd= serializers.CharField(max_length=100)

    def create(self, validated_data, pessoa_instance):
        endereco = Endereco.objects.create(**validated_data, pessoa = pessoa_instance)
        endereco.save()
        return endereco