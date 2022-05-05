# Importes de Rest framework
from rest_framework import permissions
from rest_framework import viewsets,status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from django_filters.rest_framework import DjangoFilterBackend
# Importes de Django
from django.apps import apps
from django.db.models import Count,Q,Sum
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers as sr
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse,HttpResponse,request
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Raiz
from .serializers import *
from .models import *
# Recuperar contraseña
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.urls import reverse
from django.template.loader import render_to_string
# Utiles
from django_renderpdf.views import PDFView
from email import header
from urllib import response
from numpy import indices
import pandas as pd
import csv
import requests
import datetime
""" Vistas """
class PerfilVS(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=Perfil.objects.all()
    serializer_class=PerfilSerializer
    def create(self, request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)
class DeliverVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Deliver.objects.all()
    serializer_class=DeliverSerializer
@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def verificar_perfil(request):
    data=request.data
    respuesta={}
    try:
        perfil=Perfil.objects.get(wallet__exact=data['wallet'])
        respuesta['id']=perfil.id
        respuesta['nombre']=perfil.nombre
        respuesta['wallet']=perfil.wallet
        respuesta['delivery']=perfil.delivery
        respuesta['vendedor']=perfil.vendedor
        respuesta['telefono']=perfil.telefono
        respuesta['direccion']=perfil.direccion
    except:
        respuesta['wallet']=data['wallet']
    return Response(respuesta)