from random import choices
from rest_framework import serializers
from venda.EsquemaProduto.esquema_produto_model import EsquemaProduto
from .medidas_model import Medida

class MedidaSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=50)
    validacoes = serializers.ChoiceField(choices=Medida.VALIDACOES)
    primeira_pagina = serializers.BooleanField()
    complexidade = serializers.ChoiceField(choices=Medida.COMPLEXIDADES)    
    esquema_produto = serializers.PrimaryKeyRelatedField(queryset=EsquemaProduto.objects.all(), many=False)


    def to_representation_esquema_produto(self, instance):
        return  instance.nome

    def create(self, validated_data):
        return Medida.objects.create(**validated_data)
      
    def get_validacoes(self, obj):
        return obj.get_validacoes_display()

    def get_complexidade(self, obj):
        return obj.get_complexidade_display()




    #       nome = models.CharField(max_length=50, blank=False, null=False)
    # validacoes = models.CharField(max_length= 1, choices=VALIDACOES)
    # primeira_pagina = models.BooleanField()
    # complexidade = models.IntegerField(choices=COMPLEXIDADES, null=False, blank=False)
    # esquema_produto = models.ForeignKey(EsquemaProduto, on_delete=models.CASCADE, null=False, blank=False, related_name='+')