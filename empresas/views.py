from rest_framework import generics
from .models import Empresa,Equipamento,Chamado
from .management.commands.script_geral import Command
from .serializers import EmpresaSerializer,EquipamentoSerializer,ChamadoSerializer
from django.shortcuts import render

class EmpresaList(generics.ListCreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class EquipamentoList(generics.ListCreateAPIView):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    
class ChamadoList(generics.ListCreateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer
    
def tela_principal(request):
    chamados = Chamado.objects.all()
    empresa_id, qntd_equipos, empresa_nome = Command.mais_equipos()
    nome_equipo, qntd_chamados = Command.mais_chamados()
    dict = {'chamados':chamados, 
            'empresa_id':empresa_id, 
            'qntd_equipos':qntd_equipos, 
            'empresa_nome':empresa_nome,
            'nome_equipo':nome_equipo,
            'qntd_chamados' : qntd_chamados
    }
    return render(request,"index/index.html",dict)
