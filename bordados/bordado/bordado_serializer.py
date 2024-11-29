from rest_framework import serializers
from ..imagem.Imagem_BordadoSerializer import ImagemBordado, Bordado, ImagemBordadoSerializer
from .bordado_model import Bordado, Nucleo, Particao_Especialidade
from utils.validacoes.validacoes_gerais import * 
from typing import Dict



class BordadoSerializer(serializers.Serializer):
        nome = serializers.CharField(max_length=50)
        codigo = serializers.CharField(max_length=20)
        estilo = serializers.ChoiceField(Bordado.ESTILOS)
        nucleo = serializers.PrimaryKeyRelatedField(queryset=Nucleo.objects.all())
        particao_especialidade = serializers.PrimaryKeyRelatedField(queryset=Particao_Especialidade.objects.all())
        valor = serializers.FloatField()
        imagem = serializers.ImageField()

        fields_internalizer = {
            'nome': lambda value: valida_string(value, 50, 1),
            'codigo': lambda value: valida_string(value, 20, 5),
            'valor': lambda value: valida_float(value),
            'nucleo': lambda value: valida_chave_estrangeira(value, Nucleo),
            'particao_especialidade': lambda value: valida_chave_estrangeira(value, Particao_Especialidade),
            'estilo': lambda value: valida_opcoes(value, Bordado.ESTILOS),
            'imagem': lambda value: valida_imagem(value)
        }

        fields_validation = ['nome', 'codigo']

        fields_serializers :Dict[str, type[ImagemBordadoSerializer]] = {
            'imagem': ImagemBordadoSerializer,
        } 

        fields_models :Dict[str, type[ImagemBordado]] = {
            'imagem': ImagemBordado,
        } 

        def to_representation(self, instance):
            '''
            Desserialização da instancia em objeto JSON
            '''
            fk_field = {}
            for field, serializer in self.fields_serializers.items():
                try:
                    fk_field[f'{field}'] = [
                        serializer().to_representation(instancia)
                        for instancia in self.fields_models[f'{field}'].objects.filter(bordado_id = instance.id)
                    ]
                except Exception:
                    fk_field[f'{field}'] =""
            # instance.nucleo
            # nucleo = NucleoSerializer().to_representation(instance.nucleo)
            # particao_especialidade = Particao_especialidadeSerializer().to_representation(instance.particao_especialidade)

            return {
                "nome": instance.nome,
                "codigo": instance.codigo,
                "imagem": fk_field
            }

        def to_internal_value(self, data):
            errors = {}
            internal_value = {}
            for field, validator in self.fields_internalizer.items():
                value = data.get(f'{field}')
                if not self.partial or value or value is not None:
                    try:
                        internal_value[f'{field}'] = validator(value)
                    except fieldError as e:
                        errors[f'{field}'] = e.msg
            if errors:
                raise serializers.ValidationError(errors)
            return internal_value

        def validate(self, attrs):
            errors = {}
            for field in self.fields_validation:
                filter_kwargs = {field: attrs.get(field)}
                if Bordado.objects.filter(**filter_kwargs).exists():
                    errors[field] = f"{attrs[f'{field}']} ja esta registrado em outro Bordado"
            try:        
                valida_conteudo_nucleos_particoes(attrs['nucleo'], attrs['particao_especialidade'])
            except fieldError as e:
                errors['nucleos_e_particoes'] = e.msg
            if errors:
                raise serializers.ValidationError(errors)

            return attrs

        def create(self, validated_data):
            validated_data['nucleo'] = validated_data['nucleo'][0]
            validated_data['particao_especialidade'] = validated_data['particao_especialidade'][0]
            fk_validated_data = {
                key: validated_data.pop(f'{key}')
                for key in self.fields_serializers.keys()
            }
            bordado = Bordado.objects.create(**validated_data)
            for field, serializer in self.fields_serializers.items():
                if type(fk_validated_data[f'{field}']) == []: 
                    for obj in fk_validated_data[f'{field}']:
                        serializer().create(obj, bordado)
                        continue
                dados = fk_validated_data[f'{field}']
                serializer().create(dados, bordado)
            bordado.save()
            return bordado