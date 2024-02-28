from rest_framework import serializers
from .modelagem_model import Modelagem

class ModelagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelagem
        fields = '__all__'