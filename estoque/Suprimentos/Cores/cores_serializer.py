from rest_framework import serializers
from .cores_model import Cor

class CorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cor
        fields = '__all__'