from django.core.management.base import BaseCommand
from datetime import datetime
from empresas.models import Empresa, Equipamento, Chamado
import requests
import string
import random
import json

# referência : https://docs.djangoproject.com/pt-br/2.2/howto/custom-management-commands/
class Command(BaseCommand):

    def __init__(self):
        self.URL = 'https://desenvolvimento.arkmeds.com/api/v2/'
        self.HEADER = {'Authorization': 'JWT ' +
            self.login(), 'Content-Type': 'application/json'}

    #----------------------------------------------Token de acesso-----------------------------------------------------------------------------------------#

    def login(self):
        url = "https://desenvolvimento.arkmeds.com/rest-auth/token-auth/"
        payload = json.dumps({
            "email": "a@a.com",
            "password": "a"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload).json()

        return response['token']


    #------------------------------------Métodos - equipamentos, empresas e chamados------------------------------------------------------------------------------#


    def get_empresas(self):
        response = requests.request(
            "GET", self.URL + 'empresa/', headers=self.HEADER, data='').json()
        return response


    def detalhes_empresas(self):
        companies = self.get_empresas()
        i = 0
        for company in companies:
            if i<20:
                i+=1
                id = company['id']
                empresa = requests.request(
                    "GET", self.URL + 'company/' + str(id), headers=self.HEADER, data='').json()
                if(empresa['tipo'] != 5):
                    self.salva_empresa_bd(empresa)


    def get_equipamentos(self):
        companies = self.get_empresas()
        response = []
        i=0
        for company in companies:
            if i<20:
                i+=1
                id = company['id']
                # Paginação
                next_page = self.URL + 'equipamentos_paginados/?empresa_id=' + str(id)
                while next_page is not None:
                    equipamentos = requests.request("GET", next_page, headers=self.HEADER, data='').json()['results']
                    response.append(equipamentos)
                    next_page = requests.request(
                        "GET", next_page, headers=self.HEADER, data='').json()['next']  
        return self.filtra_equipamentos(response)



    def get_chamados(self):
        lista_equipamentos = self.get_equipamentos()
        chamados = []
        for equipamento in lista_equipamentos:
            next_page = self.URL + 'chamado/?equipamento_id=' + str(equipamento['id'])
            while next_page is not None:
                chamados.append(requests.request(
                    "GET", next_page, headers=self.HEADER, data='').json())
                next_page = requests.request(
                    "GET", next_page, headers=self.HEADER, data='').json()['next']
        return self.filtra_chamados(chamados)


    def cria_chamados(self):
        texto = self.gerador_texto()
        equipamentos = self.get_equipamentos()
        for equipamento in equipamentos:
            if len(equipamento) != 0:
                payload = json.dumps({
                    "equipamento": int(equipamento['id']),
                    "solicitante": int(equipamento['proprietario']['id']),
                    "tipo_servico": 3,
                    "problema": 5,
                    "observacoes": texto,
                    "data_criacao": int(datetime.timestamp(datetime.now())),
                    "id_tipo_ordem_servico": 1
                })
                requests.request(
                    "POST", "https://desenvolvimento.arkmeds.com/api/v1/chamado/novo/", headers=self.HEADER, data=payload)


    #---------------------------------------------------Salvar no BD---------------------------------------------------------------------------------------#

    def salva_empresa_bd(self,empresa):
        Empresa(
            id=empresa['id'],
            tipo=empresa['tipo'],
            nome=empresa['nome'],
            nome_fantasia=empresa['nome_fantasia'],
            superior=empresa['superior'],
            cnpj=empresa['cnpj'],
            observacoes=empresa['observacoes'],
            contato=empresa['contato'],
            email=empresa['email'],
            telefone2=empresa['telefone2'],
            ramal2=empresa['ramal2'],
            telefone1=empresa['telefone1'],
            ramal1=empresa['ramal1'],
            fax=empresa['fax'],
            cep=empresa['cep'],
            rua=empresa['rua'],
            numero=empresa['numero'],
            complemento=empresa['complemento'],
            bairro=empresa['bairro'],
            cidade=empresa['cidade'],
            estado=empresa['estado']
        ).save()


    def salva_equipamento_bd(self,equipamento):
        Equipamento(
            id=equipamento['id'],
            fabricante=equipamento['fabricante'],
            modelo=equipamento['modelo'],
            patrimonio=equipamento['patrimonio'],
            numero_serie=equipamento['numero_serie'],
            proprietario=equipamento['proprietario']['id']
        ).save()


    def salva_chamado_bd(self,chamado):
        Chamado(
            id=chamado['id'],
            numero_chamado=chamado['chamados'],
            solocitante=chamado['get_solicitante'],
            equipamento=chamado['get_equipamento_servico'],
            prioridade=chamado['prioridade']
        ).save()

    #------------------------------------------------Funções auxiliares---------------------------------------------------------------------#

    # Referencia : https://www.horadecodar.com.br/2021/04/15/gerar-string-com-letras-e-numeros-aleatorios-em-python/

    def gerador_palavra(self):
        tamanho = 10
        chars = string.ascii_letters + string.digits
        palavra = ''.join(random.choice(chars)
                        for i in range(tamanho))  # palavras aleatórias de 10 letras
        return palavra + ' '


    def gerador_texto(self):
        tamanho = 90
        texto = ''.join(self.gerador_palavra() for i in range(tamanho))
        return texto


    def filtra_equipamentos(self,equipamentos):
        filtrado = []
        for pagina in equipamentos:
            for result in pagina:
                del result['procedimentos']
                self.salva_equipamento_bd(result)
                filtrado.append(result)
        return filtrado


    def filtra_chamados(self,chamados):
        filtrado=[]
        for chamado in chamados:
            for result in chamado['results']:
                filtrado.append(result)
                self.salva_chamado_bd(result)
        return filtrado

    # Equipamento com maior numero de chamados
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

    # Empresa com maior numero de equipamentos
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

    def handle(self,*args, **options):
        self.detalhes_empresas()
        self.get_equipamentos()
        self.cria_chamados()
        self.get_chamados()