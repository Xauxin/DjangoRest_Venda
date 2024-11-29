from rest_framework import serializers
from venda.EsquemaProduto.esquema_produto_model import EsquemaProduto
from utils.validacoes.validacoes_gerais import *
from .tamanhos_model import Tamanho

class TamanhoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=3)
    complexidade = serializers.ChoiceField(Tamanho.COMPLEXIDADES)
    esquema_produto = serializers.PrimaryKeyRelatedField(queryset=EsquemaProduto.objects.all(), many=False)

    field_validators = {
        'nome': lambda value: valida_string(value, 3, 2),
        'complexidade': lambda value : valida_opcoes(value, Tamanho.COMPLEXIDADES)
    }

    def to_internal_value(self, data):
        errors = {}
        internal_value = {}

        for field, validator in self.field_validators.items():
            value = data.get(f'{field}', "")
            try:
                internal_value[field] = validator(value)
            except fieldError as e:
                errors[f'{field}'] = e.msg
                

       
        if errors:
            raise fieldError(errors)
        
        return internal_value

    def to_representation(self, instance):
        return instance.nome

    def create(self, validated_data, esquema_instance):
        return Tamanho.objects.create(
            **validated_data, esquema_produto_id=esquema_instance.pk
        )

    def detailed_to_representation(self, instance):
        return {
            instance.nome: instance.complexidade
        }

    def update(self, instance, validated_data):
        tamanhos = Tamanho.objects.filter(esquema_produto_id = instance.pk)
        tamanhos.delete()
        for obj in validated_data:
            self.create(obj, instance)


    def get_complexidade(self, obj):
        return obj.get_complexidade_display()

    