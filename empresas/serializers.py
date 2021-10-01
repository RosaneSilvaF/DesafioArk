from rest_framework import serializers
from .models import Empresa,Equipamento,Chamado

class EmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model=Empresa
        fields='__all__'


class EquipamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Equipamento
        fields='__all__'


class ChamadoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Chamado
        fields='__all__'