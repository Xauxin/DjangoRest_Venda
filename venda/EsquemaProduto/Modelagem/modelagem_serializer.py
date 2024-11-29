from random import choices
from xml.dom import ValidationErr
from rest_framework import serializers
from utils.validacoes.validacoes_gerais import *
from venda.EsquemaProduto.Modelagem.OpcaoModelagem.opcao_modelagem_serializer import OpcaoModelagemSerializer, OpcaoModelagem
from venda.EsquemaProduto.esquema_produto_model import EsquemaProduto
from .modelagem_model import Modelagem

class ModelagemSerializer(serializers.Serializer):

    nome = serializers.CharField(max_length=50)
    requerido = serializers.BooleanField()
    tipo = serializers.ChoiceField(choices=Modelagem.TIPOS)
    esquema_produto = serializers.PrimaryKeyRelatedField(queryset=EsquemaProduto.objects.all(), many=False)
    opcoes_modelagem = serializers.DictField(allow_null=True)

    validadores_de_campos = {
        'nome': lambda value: valida_string(value, 50 , 1),
        'requerido': lambda value: valida_booleano(value),
        'tipo': lambda value: valida_opcoes(value, Modelagem.TIPOS),
        'opcoes_modelagem': lambda value: valida_lista_de_dicionarios(value, 'opcoes_modelagem', 'nome')
    }

    def to_internal_value(self, data):
        errors = {}
        internal_value = {}

        opcoes_data = data.get('opcoes_modelagem', [])

        for field, validator in self.validadores_de_campos.items():
            value = data.get(f'{field}', "")
            try:
                internal_value[field] = validator(value)
            except fieldError as e:
                errors[f'{field}'] = e.msg


        internal_opcoes = []
        if not opcoes_data:
            errors['opcoes'] = fieldError("deve ter pelo menos uma opção")
        for index , opcao in enumerate(opcoes_data):
            try:
                opcao_internal = OpcaoModelagemSerializer().to_internal_value(opcao)
                internal_opcoes.append((opcao_internal))
            except fieldError as e:
                errors[f'opcao #{index}'] = e.msg  
                        
        if errors:
            raise fieldError(errors)
        
        return internal_value

    def detailed_to_representation(self, instance):
        opcoes= OpcaoModelagem.objects.filter(modelagem = instance.id)
        dict_opcoes = {}
        for opcao in opcoes:
            dict_opcoes |= OpcaoModelagemSerializer().detailed_to_representation(opcao)
        return {
            'nome' : instance.nome,
            'requerido':('requerido' if instance.requerido else 'Não requerido'),
            'tipo' : instance.get_tipo_display(),
            'opcoes': dict_opcoes
        }


    def to_representation(self, instance):
        opcoes = OpcaoModelagem.objects.filter(modelagem = instance.id)
        list_opcoes = [
            OpcaoModelagemSerializer().to_representation(opcao) for opcao in opcoes
        ]
        return {
            'nome' : instance.nome,
            'opcoes': list_opcoes
        }

    def create(self, validated_data, esquema_instance):
        validated_data_opcoes = validated_data.pop('opcoes_modelagem', None)
        modelagem = Modelagem.objects.create(**validated_data, esquema_produto_id = esquema_instance.pk)
        for opcao in validated_data_opcoes:
            OpcaoModelagemSerializer().create(opcao, modelagem)
        modelagem.save()
        return modelagem

    def update(self, instance, validated_data):
        modelagens = Modelagem.objects.filter(esquema_produto_id = instance.pk)
        for modelagem in modelagens:
            opcoes = OpcaoModelagem.objects.filter(modelagem_id = modelagem.pk)
            opcoes.delete()
        modelagens.delete()
        for obj in validated_data:
            modelagem = self.create(obj, instance)
 



    # nome = models.CharField(max_length=50, blank=False, null=False)
    # requerido = models.BooleanField()
    # tipo = models.CharField(max_length= 1, choices=TIPOS)
    # esquema_produto = models.ForeignKey('EsquemaProduto', on_delete=models.CASCADE, null=False, blank=False, related_name='+')