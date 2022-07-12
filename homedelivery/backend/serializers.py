# Importes de  Rest Api
from collections import OrderedDict
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
    u_nombre = serializers.SerializerMethodField('nombre_usuario')
    def nombre_usuario(self, obj): 
        return obj.perfil.nombre

class ChatSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Chat
        fields = ['roomName', 'unreadCount', 'roomId', 'index', 'avatar', 'lastMessage', 'users'] 
    unreadCount = serializers.SerializerMethodField('contador')
    def contador(self, obj):
        try:
            if obj.unreadCount: return obj.unreadCount
            raise
        except: return 0
    roomId = serializers.SerializerMethodField('obtener_room')
    def obtener_room(self, obj): 
        return obj.id
    index = serializers.SerializerMethodField('obtener_index')
    def obtener_index(self, obj): 
        return obj.id
    avatar = serializers.SerializerMethodField('obtener_avatar')
    def obtener_avatar(self, obj): 
        return 'http://192.168.0.158:8080/home-delivery/img/logo.d251277d.svg'
    lastMessage = serializers.SerializerMethodField('obtener_ultimo_mensaje')
    def obtener_ultimo_mensaje(self, obj): 
        message = Mensaje.objects.filter(chat=obj).order_by('-id').first()
        if message:
            time=message.datetime.time()
            last = {
                'content': message.content, 
                'senderId': message.usuario.id, 
                'username': message.usuario.nombre if message.usuario.nombre else message.usuario.wallet, 
                'timestamp': '%s:%s'%(time.hour,time.minute if time.minute != 0 else '00' ),
                'saved': message.saved, 
                'distributed': message.distributed, 
                'seen': message.seen, 
                'new': True 
            }
        else:
            last = {
                'content': '', 
                'senderId': '', 
                'username': '', 
                'timestamp': '', 
                'saved': '', 
                'distributed': '', 
                'seen': '', 
                'new': False, 
            }
        return last
    users = serializers.SerializerMethodField('obtener_usuario')
    def obtener_usuario(self, obj): 
        usuarios = []
        for usuario in obj.usuarios.all(): 
            last_message = Mensaje.objects.filter(chat = obj.id, usuario = usuario).order_by('-id').first()
            u = {
                '_id': usuario.id,
                'username': usuario.nombre,
                'avatar': '',
                'status': {
                    'state': 'online',
                    'lastMessage': last_message.datetime if last_message else ''
                }
            }
            usuarios.append(u)
        return usuarios

class MensajeSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Mensaje
        fields = ['_id', 'indexId', 'content', 'senderId', 'username', 'avatar', 'date', 'timestamp', 'system', 'saved', 'distributed', 'seen', 'deleted', 'failure', 'disableActions', 'disableReactions', 'files', 'reactions', 'replyMessage']
    _id = serializers.SerializerMethodField('obtener_id')
    def obtener_id(self, obj): 
        return obj.id
    indexId = serializers.SerializerMethodField('obtener_indexId')
    def obtener_indexId(self, obj): 
        return obj.id
    username = serializers.SerializerMethodField('obtener_nombre')
    def obtener_nombre(self, obj): 
        return obj.usuario.nombre
    avatar = serializers.SerializerMethodField('obtener_avatar')
    def obtener_avatar(self, obj): 
        if obj.usuario.imagen: 
            return 'http://192.168.0.158:8080/home-delivery/img/logo.d251277d.svg'
        else: 
            return 'http://192.168.0.158:8080/home-delivery/img/logo.d251277d.svg'
    date = serializers.SerializerMethodField('obtener_fecha')
    def obtener_fecha(self, obj):
        return obj.datetime.date()
    timestamp = serializers.SerializerMethodField('obtener_hora')
    def obtener_hora(self, obj):
        time = obj.datetime.time()
        return '%s:%s'%(time.hour,time.minute if time.minute != 0 else '00' )
    senderId = serializers.SerializerMethodField('obtener_senderId')
    def obtener_senderId(self, obj): 
        return obj.usuario.id
    failure = serializers.SerializerMethodField('obtener_failure')
    def obtener_failure(self, obj): 
        return False
    files = serializers.SerializerMethodField('obtener_files')
    def obtener_files(self, obj): 
        return []
    reactions = serializers.SerializerMethodField('obtener_reactions')
    def obtener_reactions(self, obj): 
        return {}
    replyMessage = serializers.SerializerMethodField('obtener_replyMessage')
    def obtener_replyMessage(self, obj): 
        return None
    # reactions = serializers.SerializerMethodField('obtener_reacciones')
    # def obtener_reacciones(self, obj): 
    #     return ''
# cat crop alley rigid large giraffe wool mix lava prefer smoke genuine

class OrderSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Order
        fields = '__all__'
    client_name = serializers.SerializerMethodField('client_name_method')

    def client_name_method(self, obj):
        if type(obj) == type(OrderedDict()):
            for key, value in obj.items():
                if key == 'client':
                    return value.nombre
        return obj.client.nombre

    seller_name = serializers.SerializerMethodField('seller_name_method')
    def seller_name_method(self, obj):
        if type(obj) == type(OrderedDict()):
            for key, value in obj.items():
                if key == 'seller':
                    return value.nombre
        return obj.seller.nombre

    delivery_name = serializers.SerializerMethodField('delivery_name_method')
    def delivery_name_method(self, obj):
        if type(obj) == type(OrderedDict()):
            for key, value in obj.items():
                if key == 'delivery':
                    return value.nombre
        return obj.delivery.nombre if obj.delivery else ''

    details_count = serializers.SerializerMethodField('detail_count_method')
    def detail_count_method(self, obj):
        return OrderDetail.objects.filter(order__id=obj.id).count()

class OrderDetailSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = OrderDetail
        fields = '__all__'