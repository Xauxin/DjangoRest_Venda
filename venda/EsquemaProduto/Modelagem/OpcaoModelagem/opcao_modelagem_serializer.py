from rest_framework import serializers
from .opcao_modelagem_model import OpcaoModelagem

class OpcaoModelagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcaoModelagem
        fields = '__all__'