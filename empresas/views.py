from datetime import datetime
from django.shortcuts import render
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
    token = login()
    response = requests.request("GET",URL + 'empresa/', headers=HEADER, data='').json()
    return response

def detalhes_empresas():
    return lista_tipo('company/')
    
def get_equipamentos():
    return lista_tipo('equipamentos_paginados/?empresa_id=')

def chamado_equipamento(request):
    token = login()
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

#------------------------------------------------Funções auxiliares---------------------------------------------------------------------#

# Reference : https://www.horadecodar.com.br/2021/04/15/gerar-string-com-letras-e-numeros-aleatorios-em-python/

def gerador_palavra():
    tamanho = 10
    chars = string.ascii_letters + string.digits
    palavra = ''.join(random.choice(chars) for i in range(tamanho)) # palavras aleatórias de 10 letras
    return palavra + ' '

def gerador_texto():
    tamanho = 90
    texto = ''.join(gerador_palavra() for i in range(tamanho))
    return texto

#------------------------------------Loop principal - lista empresa e equipamentos---------------------------------------------------------------------#

def lista_tipo(sufixo):
    token = login()
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