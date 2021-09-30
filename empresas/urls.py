from django.urls import path
from .views import geral

urlpatterns = [
    path('', geral, name='geral')
]
