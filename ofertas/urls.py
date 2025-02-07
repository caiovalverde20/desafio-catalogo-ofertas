from django.urls import path
from . import views

urlpatterns = [
    path('', views.exibir_produtos, name='exibir_produtos'),
    path('atualizar/', views.atualizar_produtos, name='atualizar_produtos'),
    path('listar/', views.listar_produtos, name='listar_produtos'),
    path('listar/maior-preco/', views.listar_maior_preco, name='listar_maior_preco'),
    path('listar/menor-preco/', views.listar_menor_preco, name='listar_menor_preco'),
    path('listar/maior-desconto/', views.listar_maior_desconto, name='listar_maior_desconto'),
]
