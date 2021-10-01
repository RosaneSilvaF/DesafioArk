from django.urls import path
from .views import EmpresaList,EquipamentoList,ChamadoList

urlpatterns = [
    path('', EmpresaList.as_view(), name='empresas'),
    path('equipamentos/', EquipamentoList.as_view(), name='equipamentos'),
    path('chamados/', ChamadoList.as_view(), name='chamados'),
]
