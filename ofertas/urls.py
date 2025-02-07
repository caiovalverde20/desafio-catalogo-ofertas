from django.urls import path
from . import views

urlpatterns = [
    path('atualizar/', views.atualizar_produtos, name='atualizar_produtos'),
    path('listar/', views.listar_produtos, name='listar_produtos'),
]
