from rest_framework import status
from rest_framework.test import APITestCase   
from django.urls import reverse
from .funcoes_create import *

class EsquemaProdutoTestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse('esquema_produto-list')
        self.cor_1 = create_cor("Cor_Teste", "Tst1//tst2//tst3", "000000")
        self.suprimento_1 = create_suprimento("Suprimento_teste", 11.90, "G", "A")
        self.suprimento_1.cores.add(self.cor_1)

        self.esquema_produto_1 = create_esquema_produto(
            'Esquema Teste 1',
            "Manga Esquerda// Manga Direita// Peito",
            190.50
        )
        self.esquema_produto_1.suprimentos.add(self.suprimento_1)

        medidas_data = [
            {"nome": "teste_medida-1", "validacoes": "O", "primeira_pagina": False, "complexidade": 3},
            {"nome": "teste_medida-2", "validacoes": "A", "primeira_pagina": False, "complexidade": 2},
            {"nome": "teste_medida-3", "validacoes": "O", "primeira_pagina": False, "complexidade": 1},
            {"nome": "teste_medida-4", "validacoes": "R", "primeira_pagina": False, "complexidade": 4}
        ]
        self.medidas = {f'{index}': create_medida(**medida, esquema_produto=self.esquema_produto_1) for index, medida in enumerate(medidas_data)}

        modelagems_data = [
            {"nome": "teste4", "requerido": False, "tipo": "V", "opcoes_modelagem": [{"nome": "1245", "valor": 1245}, {"nome": "teste", "valor": 3.1419}]},
            {"nome": "teste5", "requerido": False, "tipo": "U", "opcoes_modelagem": [{"nome": "teste", "valor": 1245}]},
            {"nome": "teste6", "requerido": True, "tipo": "V", "opcoes_modelagem": [{"nome": "teste", "valor": 1245}]},
            {"nome": "12", "requerido": False, "tipo": "V", "opcoes_modelagem": [{"nome": "teste", "valor": 1245}]}
        ]

        self.modelagems = {}
        for index, modelagem_data in enumerate(modelagems_data):
            opcoes = modelagem_data.pop("opcoes_modelagem")
            modelagem = create_modelagem(**modelagem_data, esquema_produto=self.esquema_produto_1)
            self.modelagems[f'{index}'] = modelagem
            self.opcoes_modelagem = {f'{index_opcao}': create_opcao_modelagem(**opcao, modelagem=modelagem) for index_opcao, opcao in enumerate(opcoes)}

        tamanhos_data = [
            {"nome": "ste", "complexidade": 3},
            {"nome": "23", "complexidade": 2}
        ]

        self.tamanhos = {f'{index}': create_tamanho(**tamanho, esquema_produto=self.esquema_produto_1) for index, tamanho in enumerate(tamanhos_data)}

    def test_de_teste(self):
        """
        teste para testar
        """
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
