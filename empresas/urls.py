from django.contrib import admin
from django.urls import path
from .views import empresas, equipamentos

urlpatterns = [
    path('', empresas,name='empresas'),
    path('equipamentos/', equipamentos,name='equipamentos')
]
