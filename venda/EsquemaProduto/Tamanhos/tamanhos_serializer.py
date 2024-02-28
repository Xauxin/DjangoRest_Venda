from rest_framework import serializers
from .tamanhos_model import Tamanho

class TamanhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tamanho
        fields = '__all__'