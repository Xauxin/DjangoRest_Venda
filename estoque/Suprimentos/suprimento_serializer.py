from rest_framework import serializers
from .suprimento_model import Suprimento

class SuprimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suprimento
        fields = '__all__'