from rest_framework import serializers
from utils.erros import *
from utils.validacoes import validacoes_gerais, validacoes_produtos
from utils.internalizadores import internalizadores_produtos
from venda.EsquemaProduto.esquema_produto_serializer import EsquemaProduto, Tamanho, Suprimento, Medida, Modelagem
from .produto_model import Produto
from ..venda_model import Venda
from .bordado.bordado_produto_serializer import Bordado_Produto, Bordado_produtoSerializer

def internaliza_dados_de_outras_tabelas(data=None, serializer:serializers.Serializer=serializers.Serializer()):
    if data is None:
        data = []
    internal_value = []
    errors = {}

    for index, obj_data in enumerate(data):
        try:
            internal_value.append(serializer.to_internal_value(obj_data))
        except fieldError as e:
            errors[f'{index}'] = e.msg

    if errors:
        raise fieldError(errors)

    return internal_value

class ProdutoSerializer(serializers.Serializer):

    def __init__(self, instance=None, data=..., **kwargs):
        self.produto_sem_esquema = False
        if data and 'esquema' not in data:
            self.produto_sem_esquema = True
        super().__init__(instance, data, **kwargs)


    venda = serializers.PrimaryKeyRelatedField(queryset=Venda.objects.all())
    esquema = serializers.PrimaryKeyRelatedField(queryset=EsquemaProduto.objects.all())
    tecido = serializers.JSONField()
    tamanho = serializers.JSONField()
    modelagem = serializers.JSONField()
    medidas = serializers.JSONField()
    observacoes = serializers.CharField(max_length=1000)

    internalizador_campo_com_esquema = {
        'esquema' :  lambda value: validacoes_gerais.valida_chave_estrangeira(value, EsquemaProduto),
        'nome': lambda value: validacoes_gerais.valida_string(value, 50, 1),
        'tecido' :  lambda value : internalizadores_produtos.internaliza_tecido_com_esquema(value),
        'tamanho' : lambda value: internalizadores_produtos.internaliza_tamanho_com_esquema(value),
        'modelagem' : lambda value: validacoes_gerais.valida_dicionario_str_str(value),
        'medidas' : lambda value: validacoes_gerais.valida_dicionario_str_str(value),
        'bordados': lambda value: validacoes_gerais.valida_lista_de_dicionarios(value,'bordados'),
        'valor': lambda value: validacoes_gerais.valida_float(value),
        'observacoes' : lambda value: validacoes_gerais.valida_string(value,1000,0)
    }

    internalizador_campo_sem_esquema = {
        'nome': lambda value: validacoes_gerais.valida_string(value, 50, 1),
        'tecido' :  lambda value : internalizadores_produtos.internaliza_tecido_sem_esquema(value),
        'tamanho' : lambda value: internalizadores_produtos.internaliza_tamanho_sem_esquema(value),
        'modelagem' : lambda value: validacoes_gerais.valida_dicionario_str_str(value),
        'medidas' : lambda value: validacoes_gerais.valida_dicionario_str_str(value),
        'bordados': lambda value: validacoes_gerais.valida_lista_de_dicionarios(value,'bordados'),
        'valor': lambda value: validacoes_gerais.valida_float(value),
        'observacoes' : lambda value: validacoes_gerais.valida_string(value,1000,0)
    }

    validadores_com_esquema = {
        'nome': lambda  value, esquema: validacoes_produtos.valida_nome_com_esquema(value,esquema),
        'tecido': lambda  value, esquema:validacoes_produtos.valida_tecido_com_esquema(value,esquema),
        'tamanho': lambda  value, esquema:validacoes_produtos.valida_tamanho_com_esquema(value,esquema),
        'modelagem': lambda  value, esquema:validacoes_produtos.valida_modelagem_com_esquema(value,esquema),
        'medidas': lambda  value, esquema:validacoes_produtos.valida_medidas_com_esquema(value,esquema)
    }

    def get_internalizadores(self, keys=False):
        if self.produto_sem_esquema:
            return self.internalizador_campo_sem_esquema.items()
        return self.internalizador_campo_com_esquema.items()

    def get_keys_internalizadores(self):
        if self.produto_sem_esquema:
            return self.internalizador_campo_sem_esquema.keys()
        return self.internalizador_campo_com_esquema.keys()
        
    
    fields_serializers  = {
        'bordados':Bordado_produtoSerializer,
    } 

    fields_models = {
        'bordados':Bordado_Produto,
    } 

    def to_internal_value(self, data):  # sourcery skip: avoid-builtin-shadow
        """
        Converte os dados de entrada para um formato adequado para `create` e `update`.
        """
        errors = {}
        internal_value = {}
        validadores= self.get_internalizadores()
        for field, validator in validadores:
            value = data.get(f'{field}')
            if not self.partial or value or value is not None:
                try:
                    int = validator(value)
                    if field not in self.fields_serializers.keys():
                        internal_value[f'{field}'] = int
                    if (
                        field == 'esquema'
                        and not self.produto_sem_esquema
                        and 'nome' not in data
                    ):
                        data['nome'] = int.nome
                except fieldError as e:
                    errors[f'{field}'] = e.msg

        other_tables_internal_value = {}
        for field, serializer in self.fields_serializers.items():
            if field not in errors:
                value = data.get(f'{field}')
                if not self.partial or value or value is not None:
                    try:
                        internal = internaliza_dados_de_outras_tabelas(value , serializer())
                        other_tables_internal_value[f'{field}'] = internal
                    except fieldError as e:
                        errors[f'{field}'] = e.msg  

        internal_value |= other_tables_internal_value

        if errors:
            raise fieldError(msg=errors)

        return internal_value

    def validate(self, attrs):
        errors = {}
        if not self.produto_sem_esquema:
            for field, validador in self.validadores_com_esquema.items():
                value = attrs.get(field)
                if not self.partial or value or value is not None:
                    try:
                        attrs[f'{field}'] = validador(value, attrs['esquema'])
                    except fieldError as e:
                        errors[f'{field}'] = e.msg
        if errors:
            raise fieldError(msg=errors)
        print('attrs',attrs)
        return attrs


    def to_representation(self, instance):
        '''
        Desserialização da instancia em objeto JSON
        '''
        bordados_json = {}
        bordados = Bordado_Produto.objects.filter(produto_id=instance.pk)
        for indice, bordado in enumerate(bordados):
            if instance.pk == 16:
                print(bordado)
            bordados_json[indice] = Bordado_produtoSerializer().to_representation(bordado)
        print(bordados_json)
        return {
            'nome': instance.nome,
            'tecido': f"{instance.tecido['tecido_nome']}, {instance.tecido['cor_nome']}",
            'tamanho': instance.tamanho['tamanho_nome'],
            'modelagem': instance.modelagem,
            'medidas': instance.medidas or 'padrão',
            'bordados': bordados_json
        }

    def detailed_to_representation(self, instance):
        '''
        Desserialização detalhada da instancia em objeto JSON
        '''
        bordados_json = {}
        bordados = Bordado_Produto.objects.filter(produto_id=instance.pk)
        for indice, bordado in enumerate(bordados):
            if instance.pk == 16:
                print(bordado)
            bordados_json[indice] = Bordado_produtoSerializer().detailed_to_representation(bordado)
        print(bordados_json)
        return {
            'nome': instance.nome,
            'tecido': f"{instance.tecido['tecido_nome']}, {instance.tecido['cor_nome']}",
            'tamanho': instance.tamanho['tamanho_nome'],
            'modelagem': instance.modelagem,
            'medidas': instance.medidas or 'padrão',
            'bordados': bordados_json
        }

        
    def create(self, validated_data, venda_instance):
        '''
        Cria os objetos de Venda
        Juntamente cria todas as dependencias
        '''
        fk_validated_data = {
            key: validated_data.pop(f'{key}')
            for key in self.fields_serializers.keys()
        }
        produto = Produto.objects.create(**validated_data, venda = venda_instance)
        for field, serializer in self.fields_serializers.items():
            for obj in fk_validated_data[f'{field}']:
                serializer().create(obj, produto)
        produto.save()
        return produto


    def update(self, instance, validated_data):
        for field in self.get_keys_internalizadores():
            value = validated_data.get(field)
            if not self.partial or value or value is not None:    
                if field in self.get_fields().keys() and field != 'suprimentos':
                    setattr(instance, field, value)
                    instance.save()
                if field == 'suprimentos':
                    instance.suprimentos.set(value)
                    instance.save()
                if field in self.fields_serializers.keys():
                    self.fields_serializers[f'{field}']().update(instance=instance, validated_data=value)
        return instance


        



