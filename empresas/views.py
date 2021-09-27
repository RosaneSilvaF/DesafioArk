import json
from django.shortcuts import render
import requests

URL = 'https://desenvolvimento.arkmeds.com/api/v2/'
CONTENT_TYPE = 'application/json'

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

def get_empresas():
    token = login()
    response = requests.request("GET",URL + 'empresa/', headers={'Authorization':'JWT '+token, 'Content-Type': 'application/json'},data='').json()
    return response

def detalhes_empresas():
    return lista_tipo('company/')

def lista_tipo(sufixo):
    token = login()
    companies = get_empresas()
    response = []
    i=0
    for company in companies:
        if i<20:
            i+=1
            id = company['id']
            empresa = requests.request("GET", URL + 'company/' + str(id), headers={'Authorization':'JWT '+ token, 'Content-Type': CONTENT_TYPE },data='').json()
            if(empresa['tipo'] == 5):
                requests.request("DELETE", URL + 'company/' + str(id), headers={'Authorization':'JWT '+ token, 'Content-Type': CONTENT_TYPE },data='').json()
            else:
                response.append(requests.request("GET", URL + sufixo + str(id), headers={'Authorization':'JWT '+ token, 'Content-Type': CONTENT_TYPE },data='').json())
            
    return response
    
def get_equipamentos():
    return lista_tipo('equipamentos_paginados/?empresa_id=')

def empresas(request):
    response = detalhes_empresas()
    return render(request, 'empresas.html',{'response':response})

def equipamentos(request):
    response = get_equipamentos()
    return render(request, 'equipamentos.html', {'response':response})
