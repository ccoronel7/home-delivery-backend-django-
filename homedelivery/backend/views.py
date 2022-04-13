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
from django_rest_passwordreset.signals import reset_password_token_created
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
    permission_classes=[IsAuthenticated]
    queryset=Perfil.objects.all()
    serializer_class=PerfilSerializer
class DeliverVS(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Deliver.objects.all()
    serializer_class=DeliverSerializer