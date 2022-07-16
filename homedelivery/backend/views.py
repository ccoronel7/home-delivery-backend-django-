# Importes de Rest framework
from rest_framework import permissions
from rest_framework import viewsets,status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
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
from django.utils import timezone
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
class ChatVS(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=Chat.objects.all()
    serializer_class=ChatSerializer
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def list(self, request, *args, **kwargs):
        parametros = request.query_params.copy()
        usuario = Perfil.objects.get(id=parametros['usuario'])
        chats = Chat.objects.filter(usuarios=usuario)
        for c in chats:
            c.unreadCount = 0
            for m in Mensaje.objects.filter(chat=c).exclude(usuario__id=parametros['usuario']):
                if not m.seen:
                    c.unreadCount += 1
                m.distributed = True
                m.save()
        data = self.serializer_class(chats,many=True).data
        return Response(data,status=status.HTTP_200_OK)

class MensajeVS(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=Mensaje.objects.all()
    serializer_class=MensajeSerializer

    def list(self, request, *args, **kwargs):
        parametros = request.query_params.copy()
        objetos = self.queryset.filter(chat__exact=parametros['chat']).order_by('id')
        for o in objetos.exclude(usuario=parametros['usuario']):
            o.seen = True
            o.save()
        data = self.serializer_class(objetos,many=True).data
        return Response(data,status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        # Get chat and update unreadCount 
        chat = Chat.objects.get(id=data['roomId'])
        # Create msg
        indexId = self.queryset.filter(chat=chat).count() + 1
        mensaje = Mensaje.objects.create(chat=chat,usuario=Perfil.objects.get(id=data['usuario']),content=data['content'],reply_to=data['replyMessage'])
        # Serialize msg for response
        serializer = MensajeSerializer(mensaje)
        # Set Headers
        headers = self.get_success_headers(serializer.data)
        # Response
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OrderVS(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wallet_shop', 'id']
    def create(self, request):
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        data = request.data
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(data['details'])
        if (data['details']):
            total = 0.0
            for d in data['details']:
                total += data['price']
                category = []
                for c in d.category:
                    category.append(c)
                detail = OrderDetail.objects.create(
                    order=serializer.data.id,
                    contract_id=detail.contract_id, # id en el contrato
                    name=detail.name, # Nombre en el contrato
                    category=category, # Categorias asociadas en el contrato
                    price=d.price # Precio obtenido del contrato
                )
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)

class OrderDetailVS(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=OrderDetail.objects.all()
    serializer_class=OrderDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']
    def create(self, request):
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    def update(self, request,**kwargs):
        data = request.data
        order = Order.objects.get(id=data['order'])
        detail = OrderDetail.objects.get(id=data['id'])
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            details = OrderDetail.objects.filter(id=data['order'])
            new_total = 0
            for d in details:
                new_total += d.price
            order.total_price = new_total
            order.save()  
            return Response(serializer.data)
        except Exception as e:
            print(e)
            order.save()
            detail.save()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        respuesta['location']=perfil.location
        respuesta['token']='token xxx'
    except:
        respuesta['wallet']=data['wallet']
    return Response(respuesta)

@api_view(["PUT"])
@csrf_exempt
@permission_classes([AllowAny])
def update_unread(request):
    data = request.data
    chat = Chat.objects.get(id=data['chat'])
    chat.unreadCount = 0
    chat.save()
    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def order_create(request):
    data = request.data
    client=Perfil.objects.get(wallet=data['client'])
    data['client_data']="{'id':%s,'name':%s,'phone':%s,'wallet':%s}"%(client.id,client.nombre,client.telefono,client.wallet)
    seller=Perfil.objects.get(wallet=data['wallet_seller'])
    data['seller_data']="{'id':%s,'name':%s,'phone':%s,'wallet':%s}"%(seller.id,seller.nombre,seller.telefono,seller.wallet)
    pay_method=PayMethod.objects.all().first()
    pay_method_data="{'nombre':%s}"%(pay_method.name)
    order = None
    details = []
    try:
        order = Order.objects.create(
            client=client,
            client_data=data['client_data'],
            client_location=data['location'],
            # Seller,
            seller=seller,
            seller_data=data['seller_data'],
            seller_location='',
            wallet_shop=data['wallet_shop'],
            # Deliver
            delivery=None,
            delivery_data=None,
            # Metodo pago
            pay_method=pay_method,
            pay_method_data=pay_method_data,
            total_price=data['sub_total']
        )
        if (data['productos']):
            total = 0.0
            for d in data['productos']:
                total += d['price']
                categories_string = '['
                categories_string += ']'
                detail = OrderDetail.objects.create(
                    order=order,
                    # contract_id=d['contract_id'], # id en el contrato
                    name=d['name'], # Nombre en el contrato
                    # category=categories_string, # Categorias asociadas en el contrato
                    price=d['price'], # Precio obtenido del contrato
                    comment=d['comment']
                )
                if detail.id:
                    details.append(detail)
        # chat = Chat.objects.create(usuarios=[client,seller])
        serializer = OrderSerializer(order)
        serializer2 = OrderDetailSerializer(detail)
        # headers = {'Location': str(data[api_settings.URL_FIELD_NAME])}
        return Response({"orden":serializer.data, "odetail":serializer2.data},status=status.HTTP_201_CREATED) # headers=headers
    except Exception as e:
        print(e)
        if order:
            if order.id:
                order.delete()
        for d in details:
            OrderDetail.objects.get(id=d).delete()
        return Response('%s'%(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR) # headers=headers

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def order_update_deliver(request):
    try:
        data = request.data
        delivery=Perfil.objects.get(id=data['delivery'])
        if delivery.delivery:
            data['delivery_data']="{'id':%s,'name':%s,'phone':%s,'wallet':%s}"%(delivery.id,delivery.nombre,delivery.telefono,delivery.wallet)
            order = Order.objects.get(id=data['id'])
            order.delivery = delivery
            order.delivery_data = data['delivery_data']
            order.save()
            # headers = {'Location': str(data[api_settings.URL_FIELD_NAME])}
            serializer = OrderSerializer(order)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response('El usuario solicitado no es un delivery',status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        print(e)
        return Response('Ha ocurrido un error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def order_update_cancel (request):
    try:
        data = request.data
        order = Order.objects.get(id=data['id'])
        # if client.usuario == usuario or seller.usuario == usuario:
        order.raison_cancel = data['razon']
        order.statu = 'X'
        order.save()
        # headers = {'Location': str(data[api_settings.URL_FIELD_NAME])}
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response('Ha ocurrido un error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def order_update_statu(request):
    try:
        data = request.data
        order = Order.objects.get(id=data['id'])
        # if order.client.usuario == usuario or order.seller.usuario == usuario:
        order.statu = data['statu']
        order.save()
        # headers = {'Location': str(data[api_settings.URL_FIELD_NAME])}
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response('Ha ocurrido un error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def pending_orders_client_side(request):
    try:
        params = request.query_params.copy()
        if not params.get('id',None):
            return Response('Falta pasar como parametro el "id" del cliente',status=status.HTTP_406_NOT_ACCEPTABLE)
        orders = Order.objects.filter(client=params['id']).exclude(statu='X').exclude(statu='E')
        # headers = {'Location': str(data[api_settings.URL_FIELD_NAME])}
        serializer = PendingOrdersSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response('Ha ocurrido un error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
