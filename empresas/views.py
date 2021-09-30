from empresas.scripts.script_geral import cria_chamados, salva_equipamentos_bd, salva_empresas_bd, salva_chamados_bd
from django.shortcuts import render

def geral(request):
    salva_empresas_bd()
    salva_equipamentos_bd()
    cria_chamados()
    salva_chamados_bd()
    response = 'rosane'
    return render(request, 'empresas.html', {'response':response})