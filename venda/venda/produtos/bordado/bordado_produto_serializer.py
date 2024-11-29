from rest_framework import serializers
from ..produto_model import Produto
from utils.validacoes.validacoes_gerais import *
from .bordado_produto_model import Bordado_Produto, Bordado

class Bordado_produtoSerializer(serializers.Serializer):
    produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all())
    bordado = serializers.PrimaryKeyRelatedField(queryset=Bordado.objects.all())
    local = serializers.CharField(max_length=50)

    field_validators = {
        'local': lambda value: valida_string(value, 50, 5),
        'bordado' : lambda value: valida_chave_estrangeira(value, Bordado)
    
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


    def create(self, validated_data, produto_instance):
        return Bordado_Produto.objects.create(
            **validated_data, produto_id=produto_instance.pk
        )

    def to_representation(self, instance):
        bordado = Bordado.objects.get(pk = instance.bordado_id)
        return bordado.nome
    
    
    def detailed_to_representation(self, instance):
        bordado = Bordado.objects.get(pk = instance.bordado_id)
        return f'{bordado.nome} - {instance.local}'
        
        
    def update(self, instance, validated_data):
        bordado_produtos = Bordado_Produto.objects.filter(produto_id = instance.pk)
        bordado_produtos.delete()
        for obj in validated_data:
            self.create(obj, instance)

    