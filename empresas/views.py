from datetime import datetime
from django.shortcuts import render
from .models import Empresa, Equipamento, Chamado
import requests
import string
import random
import json

#------------------------------------Token de acesso e variáveis globais------------------------------------------------------------------------------#

def login():
    url = "https://desenvolvimento.arkmeds.com/rest-auth/token-auth/"
    payload = json.dumps({
        "email": "a@a.com",
        "password": "a"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    
    return response['token']

URL = 'https://desenvolvimento.arkmeds.com/api/v2/'
HEADER = {'Authorization': 'JWT '+ login(),'Content-Type': 'application/json'}

#------------------------------------Métodos dos equipamentos e empresas------------------------------------------------------------------------------#

def get_empresas():
    response = requests.request("GET",URL + 'empresa/', headers=HEADER, data='').json()
    return response

def detalhes_empresas():
    return lista_tipo('company/')
    
def get_equipamentos():
    return lista_tipo('equipamentos_paginados/?empresa_id=')

def chamado_equipamento(request):
    response = []
    texto = gerador_texto()
    equipamentos = get_equipamentos()
    for equipamento in equipamentos: 
        if len(equipamento['results']) != 0:
            payload = json.dumps({
                "equipamento" : int(equipamento['results'][0]['id']),
                "solicitante": int(equipamento['results'][0]['proprietario']['id']),
                "tipo_servico": 3,
                "problema": 5,
                "observacoes": texto,
                "data_criacao": int(datetime.timestamp(datetime.now())),
                "id_tipo_ordem_servico": 1
            })
            response.append(requests.request("POST", "https://desenvolvimento.arkmeds.com/api/v1/chamado/novo/", headers=HEADER, data=payload))
    return render(request, 'chamados.html',{'response':response})

def empresas(request):
    response = detalhes_empresas()
    return render(request, 'empresas.html',{'response':response})

def equipamentos(request):
    response = get_equipamentos()
    return render(request, 'equipamentos.html', {'response':response})

#------------------------------------Loop principal - lista empresa e equipamentos---------------------------------------------------------------------#

def lista_tipo(sufixo):
    companies = get_empresas()
    response = []
    i=0
    for company in companies:
        if i<20:
            i+=1
            id = company['id']
            empresa = requests.request("GET", URL + 'company/' + str(id), headers=HEADER, data='').json()
            if(empresa['tipo'] == 5):
                requests.request("DELETE", URL + 'company/' + str(id), headers=HEADER, data='').json()
            else:
                response.append(requests.request("GET", URL + sufixo + str(id), headers=HEADER, data='').json())
            
    return response

#---------------------------------------------------Salvar no BD---------------------------------------------------------------------------------------#

def salva_empresas_bd():
    lista_empresas = detalhes_empresas()
    for empresa in lista_empresas:
        Empresa(
            id = empresa['id'],
            tipo = empresa['tipo'],
            nome = empresa['nome'],
            nome_fantasia = empresa['nome_fantasia'],
            superior = empresa['superior'],
            cnpj = empresa['cnpj'],
            observacoes = empresa['observacoes'],
            contato = empresa['contato'],
            email = empresa['email'],
            telefone2 = empresa['telefone2'],
            ramal2 = empresa['ramal2'],
            telefone1 = empresa['telefone1'],
            ramal1 = empresa['ramal1'],
            fax = empresa['fax'],
            cep = empresa['cep'],
            rua = empresa['rua'],
            numero = empresa['numero'],
            complemento = empresa['complemento'],
            bairro = empresa['bairro'],
            cidade = empresa['cidade'],
            estado = empresa['estado']
        ).save()


def salva_equipamentos_bd():
    lista_equipamentos = get_equipamentos()['results']
    for equipamento in lista_equipamentos:
        Equipamento(
            id = equipamento['id'],
            fabricante = equipamento['fabricante'],
            modelo = equipamento['modelo'],
            patrimonio = equipamento['patrimonio'],
            numero_serie = equipamento['numero_serie'],
            proprietario = equipamento['proprietario']['id']
        ).save()

def salva_chamados_bd():
    lista_equipamentos = get_equipamentos()['results']
    chamado = None
    for equipamento in lista_equipamentos:
        chamado = requests.request("GET", URL + 'chamado/?equipamento_id=' + equipamento['id'], headers=HEADER, data='').json()
        print(chamado)
        Chamado(
            id = chamado['id'],
            numero_chamado = chamado['chamados'],
            solocitante = chamado['get_solicitante'],
            equipamento = chamado['get_equipamento_servico'],
            prioridade = chamado['prioridade']
        ).save()

#------------------------------------------------Funções auxiliares---------------------------------------------------------------------#

# Referencia : https://www.horadecodar.com.br/2021/04/15/gerar-string-com-letras-e-numeros-aleatorios-em-python/

def gerador_palavra():
    tamanho = 10
    chars = string.ascii_letters + string.digits
    palavra = ''.join(random.choice(chars) for i in range(tamanho)) # palavras aleatórias de 10 letras
    return palavra + ' '

def gerador_texto():
    tamanho = 90
    texto = ''.join(gerador_palavra() for i in range(tamanho))
    return texto
