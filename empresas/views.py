from rest_framework import generics
from .models import Empresa,Equipamento,Chamado
from .serializers import EmpresaSerializer,EquipamentoSerializer,ChamadoSerializer

class EmpresaList(generics.ListCreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class EquipamentoList(generics.ListCreateAPIView):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    
class ChamadoList(generics.ListCreateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer
    


# def geral(request):
#     salva_empresas_bd()
#     salva_equipamentos_bd()
#     cria_chamados()
#     salva_chamados_bd()
#     response = 'rosane'
#     return render(request, 'empresas.html', {'response':response})