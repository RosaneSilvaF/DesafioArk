from django.contrib import admin
from django.urls import path
from .views import empresas, equipamentos,chamado_equipamento

urlpatterns = [
    path('', empresas,name='empresas'),
    path('equipamentos/', equipamentos,name='equipamentos'),
    path('chamados/',chamado_equipamento,name='chamados')
]
