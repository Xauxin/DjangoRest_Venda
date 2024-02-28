from rest_framework import serializers
from .medidas_model import Medida

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'