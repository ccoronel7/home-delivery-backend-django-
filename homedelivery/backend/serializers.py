# Importes de  Rest Api
from rest_framework import fields, serializers
# Importes de Django
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
# Raiz
from .models import *
""" Clases creadas para rest api """
# Contenido base
class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model=Perfil
        fields='__all__'
class DeliverSerializer(serializers.ModelSerializer):
    class Meta:
        model=Deliver
        fields='__all__'
    u_nombre=serializers.SerializerMethodField('nombre_usuario')
    def nombre_usuario(self, obj):
        return obj.perfil.nombre