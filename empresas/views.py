from rest_framework import generics
from .models import Empresa,Equipamento,Chamado
from .management.commands.script_geral import Command
from django.views.generic import TemplateView
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

class GeneralView(TemplateView):
    template_name = "index/index.html"

    def get_context_data(self, **kwargs):
        empresa_id, qntd_equipos, empresa_nome = Command.mais_equipos()
        nome_equipo, qntd_chamados = Command.mais_chamados()
        context = super(GeneralView, self).get_context_data(**kwargs)
        
        context['chamados'] = Chamado.objects.all()
        context['empresa_id'] = empresa_id
        context['qntd_equipos'] = qntd_equipos
        context['empresa_nome'] = empresa_nome
        context['nome_equipo'] = nome_equipo
        context['qntd_chamados'] = qntd_chamados
        
        return context