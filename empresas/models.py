from django.db import models

class Empresa(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.IntegerField()
    nome = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100,null=True)
    superior = models.CharField(max_length=100, null=True)
    cnpj = models.CharField(max_length=20,null=True)
    observacoes = models.TextField(null=True)
    contato = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    telefone2 = models.CharField(max_length=20,null=True)
    ramal2 = models.CharField(max_length=20,null=True)
    telefone1 = models.CharField(max_length=20,null=True)
    ramal1 = models.CharField(max_length=20,null=True)
    fax = models.CharField(max_length=20,null=True)
    cep = models.CharField(max_length=20,null=True)
    rua = models.CharField(max_length=100,null=True)
    numero = models.CharField(max_length=20,null=True)
    complemento = models.CharField(max_length=100,null=True)
    bairro = models.CharField(max_length=100,null=True)
    cidade = models.CharField(max_length=100,null=True)
    estado = models.CharField(max_length=100,null=True)

class Equipamento(models.Model):
    id = models.IntegerField(primary_key=True)
    fabricante = models.CharField(max_length=100,null=True)
    modelo = models.CharField(max_length=100,null=True)
    patrimonio = models.CharField(max_length=100,null=True)
    numero_serie = models.CharField(max_length=50,null=True)
    proprietario = models.IntegerField(blank=False,null=True)

class Chamado(models.Model):
    id = models.IntegerField(primary_key=True)
    numero_chamado = models.IntegerField()
    solocitante = models.CharField(max_length=100)
    equipamento = models.CharField(max_length=100)
    prioridade = models.IntegerField()