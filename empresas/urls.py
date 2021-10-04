from django.urls import path
from .views import EmpresaList,EquipamentoList,ChamadoList, tela_principal

urlpatterns = [
    path('', tela_principal, name='index'),
    path('empresas/', EmpresaList.as_view(), name='empresas'),
    path('equipamentos/', EquipamentoList.as_view(), name='equipamentos'),
    path('chamados/', ChamadoList.as_view(), name='chamados'),
]
