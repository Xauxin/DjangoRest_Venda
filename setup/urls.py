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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from pessoas.Particao_Especialidade.particao_especialidade_views import Particao_especialidadeViewSet, Particao_especialidade_por_nucleoViewSet
from pessoas.pessoas.pessoa_views import PessoaViewSet, NucleoComParticoesPorPessoaViewSet
from venda.EsquemaProduto.esquema_produto_view import EsquemaProdutoViewSet
from estoque.Suprimentos.suprimento_view import SuprimentoViewset
from estoque.Suprimentos.Cores.cores_view import CorViewset
from pessoas.nucleo.nucleo_views import NucleoComParticoesViewSet, NucleoViewSet
from bordados.bordado.bordado_views import BordadoViewSet
from venda.venda.venda_views import VendaViewSet


router = routers.DefaultRouter()
router.register('venda', VendaViewSet, "venda")
router.register('particao_especialidade', Particao_especialidadeViewSet, basename= 'particao_especialidade')
router.register('esquema_produto', EsquemaProdutoViewSet, basename= 'esquema_produto')
router.register('suprimento', SuprimentoViewset, basename= 'Suprimento')
router.register('cor', CorViewset, basename= 'Cor')
router.register("nucleo", NucleoViewSet, basename='nucleo')
router.register("nucleo-particoes", NucleoComParticoesViewSet, basename="nucleo_particoes")
router.register('pessoa', PessoaViewSet, basename='pessoa')
router.register('bordado', BordadoViewSet, basename='bordado')





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('pessoa/<int:pk>/nucleos-particoes', NucleoComParticoesPorPessoaViewSet.as_view({'get':'retrieve'}), name='nucleo_particoes_pessoa'),
    path('pessoas/<str:pk_list>/nucleos-particoes', NucleoComParticoesPorPessoaViewSet.as_view({'get':'list'}), name='nucleo_particoes_pessoa'),
    path('particao_especialidade-por-nucleo', Particao_especialidade_por_nucleoViewSet.as_view({'get':'list'}), name='particoes_especialidade_por_nucleo')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

