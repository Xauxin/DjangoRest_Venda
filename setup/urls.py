"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from venda.EsquemaProduto.esquema_produto_view import EsquemaProdutoViewset
from venda.EsquemaProduto.Medidas.medidas_view import MedidaViewset
from venda.EsquemaProduto.Modelagem.modelagem_view import ModelagemViewset
from venda.EsquemaProduto.Modelagem.OpcaoModelagem.opcao_modelagem_view import OpcaoModelagemViewset
from venda.EsquemaProduto.Tamanhos.tamanhos_view import TamanhoViewset
from estoque.Suprimentos.suprimento_view import SuprimentoViewset
from estoque.Suprimentos.Cores.cores_view import CorViewset


router = routers.DefaultRouter()
router.register('esquema_produto', EsquemaProdutoViewset, 'Esquema Produto')
router.register('suprimento', SuprimentoViewset, 'Suprimento')
router.register('cor', CorViewset, 'Cor')
router.register('medida', MedidaViewset, 'Medida')
router.register('modelagem', ModelagemViewset, 'Modelagem')
router.register('tamanho', TamanhoViewset, 'Tamanho')
router.register('opcao_modelagem', OpcaoModelagemViewset, 'Opcao Modelgem')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
