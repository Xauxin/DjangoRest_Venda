from rest_framework import serializers
from .esquema_produto_model import EsquemaProduto

class EsquemaProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EsquemaProduto
        fields = '__all__'