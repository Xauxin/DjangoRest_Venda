from random import choices
from rest_framework import serializers
from venda.EsquemaProduto.esquema_produto_model import EsquemaProduto
from utils.validacoes.validacoes_gerais import *
from .medidas_model import Medida


class MedidaSerializer(serializers.Serializer):

    nome = serializers.CharField(max_length=50)
    validacoes = serializers.ChoiceField(choices=Medida.VALIDACOES)
    primeira_pagina = serializers.BooleanField()
    complexidade = serializers.ChoiceField(choices=Medida.COMPLEXIDADES)    
    esquema_produto = serializers.PrimaryKeyRelatedField(queryset=EsquemaProduto.objects.all(), many=False)

    validadores_de_campos = {
        'nome': lambda value: valida_string(value, 50 , 1),
        'validacoes': lambda value: valida_opcoes(value, Medida.VALIDACOES),
        'primeira_pagina': lambda value: valida_booleano(value),
        'complexidade': lambda value: valida_opcoes(value, Medida.COMPLEXIDADES),
    }


    def to_representation(self, instance):
        return  instance.nome,

    def detailed_to_representation(self, instance):
        return  {
            "nome":instance.nome,
            'validacoes': instance.validacoes,
            'primeira_pagina': instance.primeira_pagina,
            'complexidade': instance.complexidade
        }

    def to_internal_value(self, data):
        errors = {}
        internal_value = {}

        for field, validator in self.validadores_de_campos.items():
            value = data.get(f'{field}', "")
            try:
                internal_value[field] = validator(value)
            except fieldError as e:
                errors[f'{field}'] = e.msg
                

       
        if errors:
            raise fieldError(errors)
        
        return internal_value

    def create(self, validated_data, esquema_instance):
        return Medida.objects.create(
            **validated_data, esquema_produto_id=esquema_instance.pk
        )

    def update(self, instance, validated_data):
        medidas = Medida.objects.filter(esquema_produto_id = instance.pk)
        medidas.delete()
        for obj in validated_data:
            self.create(obj, instance)


    def get_validacoes(self, obj):
        return obj.get_validacoes_display()

    def get_complexidade(self, obj):
        return obj.get_complexidade_display()




    #       nome = models.CharField(max_length=50, blank=False, null=False)
    # validacoes = models.CharField(max_length= 1, choices=VALIDACOES)
    # primeira_pagina = models.BooleanField()
    # complexidade = models.IntegerField(choices=COMPLEXIDADES, null=False, blank=False)
    # esquema_produto = models.ForeignKey(EsquemaProduto, on_delete=models.CASCADE, null=False, blank=False, related_name='+')