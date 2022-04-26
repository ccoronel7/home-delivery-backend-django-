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
        model = Perfil
        fields = '__all__'
class DeliverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliver
        fields = '__all__'
    u_nombre = serializers.SerializerMethodField('LoadNombreUsuario')
    def LoadNombreUsuario(self, obj):
        return obj.usuario.nombre
class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = '__all__'
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
class DetalleProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleProducto
        fields = '__all__'