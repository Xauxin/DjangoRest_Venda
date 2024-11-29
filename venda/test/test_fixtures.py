from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import json
from estoque.Suprimentos.suprimento_serializer import *
from venda.EsquemaProduto.esquema_produto_serializer import EsquemaProduto


class FixtureDataTestCase(TestCase):

    fixtures = ['teste_json.json']
    resposta_esperada_Esquema_1_resumido = {'nome': 'Jaleco Masculino', 'suprimentos': ['Gabardine Sintra', 'Botao', 'Linha', 'Fio', 'Entretela', 'TicTac', 'Zíper Invisível'], 'modelagens': [{'nome': 'Gola', 'opcoes': ['Blaser', 'Padre', 'Smoking']}, {'nome': 'Bolso', 'opcoes': ['com', 'Com']}, {'nome': 'Trava', 'opcoes': ['Presa']}, {'nome': 'Vivo', 'opcoes': []}, {'nome': 'manga', 'opcoes': []}, {'nome': 'punho', 'opcoes': []}], 'tamanhos': ['38', '40', '42', '44', '46', '48', '50', '52', '54', '56', '58', '60'], 'medidas': [['busto'], ['comprimento'], ['bordado'], ['comprimento Manga'], ['- de cv a br'], ['frente'], ['menos do lado']], 'locais_de_bordado_sugeridos': 'Manga Esqueda//Manga Direita//Peito', 'valor_base': 170.0}
    resposta_esperada_Esquema_1_detalhado = {'nome': 'Jaleco Masculino', 'suprimentos': [{'nome': 'Gabardine Sintra', 'cores': ['Silver', 'Grafite', 'Hortencia', 'Azul Noite', 'Preto']}, {'nome': 'Botao', 'cores': ['Céu', 'Acqua', 'Silver', 'Plácido', 'Preto', 'Brnco']}, {'nome': 'Linha', 'cores': ['Azul Noite', 'Lunar', 'Beje', 'Céu', 'Acqua', 'Silver', 'Grafite', 'Plácido', 'Lilás', 'Uva', 'Hortencia', 'Laranja', 'Cereja', 'Verde Bandeira', 'Verde Militar', 'Cobalto', 'Denin', 'Azul Noite', 'Preto', 'Brnco']}, {'nome': 'Fio', 'cores': ['Azul Noite', 'Lunar', 'Beje', 'Céu', 'Acqua', 'Silver', 'Grafite', 'Plácido', 'Lilás', 'Uva', 'Hortencia', 'Laranja', 'Cereja', 'Verde Bandeira', 'Verde Militar', 'Cobalto', 'Denin', 'Azul Noite', 'Preto', 'Brnco']}, {'nome': 'Entretela', 'cores': ['Preto', 'Brnco']}, {'nome': 'TicTac', 'cores': ['Céu', 'Acqua', 'Silver', 'Plácido', 'Preto', 'Brnco']}, {'nome': 'Zíper Invisível', 'cores': ['Azul Noite', 'Lunar', 'Beje', 'Céu', 'Acqua', 'Silver']}], 'modelagens': [{'nome': 'Gola', 'requerido': 'requerido', 'tipo': 'Unico', 'opcoes': {'Blaser': 0.0, 'Padre': 5.0, 'Smoking': 20.0}}, {'nome': 'Bolso', 'requerido': 'requerido', 'tipo': 'Unico', 'opcoes': {'com': 0.0, 'Com': 10.0}}, {'nome': 'Trava', 'requerido': 'requerido', 'tipo': 'Unico', 'opcoes': {'Presa': 0.0}}, {'nome': 'Vivo', 'requerido': 'Não requerido', 'tipo': 'Varias Escolhas', 'opcoes': {}}, {'nome': 'manga', 'requerido': 'requerido', 'tipo': 'Unico', 'opcoes': {}}, {'nome': 'punho', 'requerido': 'requerido', 'tipo': 'Unico', 'opcoes': {}}], 'tamanhos': [{'38': 2}, {'40': 2}, {'42': 2}, {'44': 2}, {'46': 2}, {'48': 2}, {'50': 3}, {'52': 3}, {'54': 3}, {'56': 3}, {'58': 3}, {'60': 3}], 'medidas': [{'nome': 'busto', 'validacoes': 'O', 'primeira_pagina': True, 'complexidade': 2}, {'nome': 'comprimento', 'validacoes': 'O', 'primeira_pagina': True, 'complexidade': 3}, {'nome': 'bordado', 'validacoes': 'A', 'primeira_pagina': True, 'complexidade': 1}, {'nome': 'comprimento Manga', 'validacoes': 'O', 'primeira_pagina': True, 'complexidade': 3}, {'nome': '- de cv a br', 'validacoes': 'O', 'primeira_pagina': False, 'complexidade': 3}, {'nome': 'frente', 'validacoes': 'o', 'primeira_pagina': True, 'complexidade': 2}, {'nome': 'menos do lado', 'validacoes': 'O', 'primeira_pagina': False, 'complexidade': 4}], 'locais_de_bordado_sugeridos': 'Manga Esqueda//Manga Direita//Peito', 'valor_base': 170.0}
    resposta_esperada_Esquema_1_fail = {    "nome": "O Campo não pode ser vazio ou nulo",    "locais_de_bordado_sugeridos": "O Campo não pode ser vazio ou nulo",    "valor_base": "O campo não pode ser vazio ou nulo",    "suprimentos": "A lista não pode estar vazia",    "medidas": "Este campo não pode ser nulo nem vazio",    "modelagens": "Este campo não pode ser nulo nem vazio",    "tamanhos": "Este campo não pode ser nulo nem vazio"}
    data_post_valido = {'nome': 'Esquema Teste 2',"locais_de_bordado_sugeridos": "Parte 1// Parte 2","valor_base": 250.75,"suprimentos": [1,2,3],"modelagens":[{"nome": "Gola","requerido": True,"tipo": "U","opcoes_modelagem":[{    "nome": "Blaser",    "valor": 1},{    "nome": "Padre",    "valor": 10},{"nome": "Smoking","valor": 20}]}],"tamanhos":[{"nome": "38","complexidade": 2},{"nome": "40","complexidade": 2},{"nome": "42","complexidade": 2},{"nome": "44","complexidade": 2}],"medidas":[{"nome": "menos do lado","validacoes": "O","primeira_pagina": False,"complexidade": 4}]}
    data_post_nome_repetido = {'nome': 'Jaleco Masculino',"locais_de_bordado_sugeridos": "Parte 1// Parte 2","valor_base": 250.75,"suprimentos": [1,2,3],"modelagens":[{"nome": "Gola","requerido": True,"tipo": "U","opcoes_modelagem":[{    "nome": "Blaser",    "valor": 1},{    "nome": "Padre",    "valor": 10},{"nome": "Smoking","valor": 20}]}],"tamanhos":[{"nome": "38","complexidade": 2},{"nome": "40","complexidade": 2},{"nome": "42","complexidade": 2},{"nome": "44","complexidade": 2}],"medidas":[{"nome": "menos do lado","validacoes": "O","primeira_pagina": False,"complexidade": 4}]}
    data_post_invalido =  {"nome": "","locais_de_bordado_sugeridos": "Parte 1// Parte 2~lkgnnergkergoiengóingergerewfrerwerwerr","valor_base": -10.75,"suprimentos": [],"tamanhos": "34","medidas": ["busto", "comprimento"]}
    data_patch_valido = {"nome": "Jaleco Masculino Diferente", "valor_base": 199}
    def setUp(self):
        self.list_url = reverse('esquema_produto-list')
        self.detail_url = lambda pk: reverse('esquema_produto-detail', kwargs={'pk': pk})
        self.esquema_produto_1 = EsquemaProduto.objects.get(id=1)
        self.suprimento_1 = Suprimento.objects.get(id=1)
        self.esquemas_len = len(EsquemaProduto.objects.all())
        # print(f"cores : {len(Cor.objects.all())} criadas")
        # print(f"suprimentos : {len(Suprimento.objects.all())} criados")
        # print(f"esquemaProdutos : {len(EsquemaProduto.objects.all())} criados")
        # print(f"medidas : {len(Medida.objects.all())} criados")
        # print(f"modelagems : {len(Modelagem.objects.all())} criados")
        # print(f"tamanhos : {len(Tamanho.objects.all())} criados")

    def test_list_esquema_produtos(self):
        """
        Testa a listagem de todos os esquemas de produtos
        """
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
        self.assertEquals(len(response.json()) , self.esquemas_len)
        self.assertEquals(response.json()[0] , self.resposta_esperada_Esquema_1_resumido)
        self.assertIn('nome', response.json()[0])
        self.assertIn('suprimentos', response.json()[0])

    def test_retrieve_esquema_produto(self):
        """
        Testa a recuperação de um esquema de produto específico por ID
        """
        response = self.client.get(self.detail_url(self.esquema_produto_1.pk))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), self.resposta_esperada_Esquema_1_detalhado)

    def test_retrieve_esquema_produto_inexistente(self):
        """ 
        Testa a recuperação de um esquema de produto inexistente
        """
        response = self.client.get(self.detail_url(999))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_esquema_produto(self):
        """
        Testa a criação de um novo esquema de produto
        """
        response = self.client.post(self.list_url, self.data_post_valido, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['nome'], self.data_post_valido['nome'])

    def test_create_esquema_produto_com_nome_ja_existente(self):
        """
        Teste a criação de Esquema com nome ja existente
        """

        response = self.client.post(self.list_url, self.data_post_nome_repetido, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_esquema_produto_dados_invalidos(self):
        """
        Testa a criação de um esquema de produto com dados inválidos
        """
        response = self.client.post(self.list_url, self.data_post_invalido,content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.json(), self.resposta_esperada_Esquema_1_fail)

    def test_update_esquema_produto(self):
        """
        Testa a atualização de um esquema de produto existente
        """        
        response = self.client.put(self.detail_url(self.esquema_produto_1.pk), self.data_post_valido, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['nome'], self.data_post_valido['nome'])

    def test_update_esquema_produto_dados_invalidos(self):
        """
        Testa a atualização de um esquema de produto com dados inválidos
        """
        response = self.client.put(self.detail_url(self.esquema_produto_1.pk), self.data_post_invalido, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_esquema_produto_pk_invalida(self):
        """
        Testa a atualização de um esquema de produto com pk/id errado
        """
        response = self.client.put(self.detail_url(999), self.data_post_valido, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_parcial_update_esquema_produto(self):
        """
        Testa a atualização de um esquema de produto com pk/id errado
        """
        response = self.client.patch(self.detail_url(self.esquema_produto_1.pk), self.data_patch_valido, content_type='application/json')
        self.assertNotEquals(self.esquema_produto_1.nome, response.json()['nome'])


    def test_delete_esquema_produto(self):
        """
        Testa a exclusão de um esquema de produto existente
        """
        response = self.client.delete(self.detail_url(self.esquema_produto_1.pk))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.detail_url(self.esquema_produto_1.pk))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_esquema_produto_inexistente(self):
        """
        Testa a exclusão de um esquema de produto inexistente
        """
        response = self.client.delete(self.detail_url(999))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)