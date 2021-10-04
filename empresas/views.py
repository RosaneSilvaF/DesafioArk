from rest_framework import generics
from .models import Empresa,Equipamento,Chamado
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
    empresa_id, qntd_equipos, empresa_nome = mais_equipos()
    nome_equipo, qntd_chamados = mais_chamados()
    dict = {'chamados':chamados, 
            'empresa_id':empresa_id, 
            'qntd_equipos':qntd_equipos, 
            'empresa_nome':empresa_nome,
            'nome_equipo':nome_equipo,
            'qntd_chamados' : qntd_chamados
    }
    return render(request,"index/index.html",dict)

def mais_chamados():
    qntd_chamados=0
    #Lista de equipamentos que tem chamados
    list_equipos = list(Chamado.objects.all().values('equipamento'))
    equipamentos = []
    for equipo in list_equipos:
        equipamentos.append(equipo['equipamento'])

    #retirada das informações
    for nome in equipamentos:
        if qntd_chamados < equipamentos.count(nome):
            nome_equipo = nome
            qntd_chamados = equipamentos.count(nome)
    return nome_equipo, qntd_chamados

def mais_equipos():
    qntd_equipos=0
    #Lista de ids das empresas que tem equipamentos
    list_proprietarios = list(Equipamento.objects.all().values('proprietario'))
    empresas = []
    for empresa in list_proprietarios:
        empresas.append(empresa['proprietario'])

    #retirada das informações
    for id in empresas:
        if qntd_equipos < empresas.count(id):
            empresa_id = id
            qntd_equipos = empresas.count(id)
    empresa_nome = Empresa.objects.get(id=empresa_id).nome
    return empresa_id, qntd_equipos,empresa_nome