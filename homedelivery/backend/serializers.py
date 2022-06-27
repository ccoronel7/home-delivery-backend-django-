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
    u_nombre = serializers.SerializerMethodField('nombre_usuario')
    def nombre_usuario(self, obj): 
        return obj.perfil.nombre

class ChatSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Chat
        fields = ['roomName', 'unreadCount', 'roomId', 'index', 'avatar', 'lastMessage', 'users'] 

    roomId = serializers.SerializerMethodField('obtener_room')
    def obtener_room(self, obj): 
        return obj.id
    index = serializers.SerializerMethodField('obtener_index')
    def obtener_index(self, obj): 
        return obj.id
    avatar = serializers.SerializerMethodField('obtener_avatar')
    def obtener_avatar(self, obj): 
        return 'http://192.168.0.158:8081/home-delivery/img/logo.d251277d.svg'
    lastMessage = serializers.SerializerMethodField('obtener_ultimo_mensaje')
    def obtener_ultimo_mensaje(self, obj): 
        message = Mensaje.objects.filter(chat=obj).order_by('-id').first()
        if message:
            last = {
                'content': message.content, 
                'senderId': message.usuario.id, 
                'username': message.usuario.nombre if message.usuario.nombre else message.usuario.wallet, 
                'timestamp': message.timestamp, 
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
                    'lastMessage': last_message.timestamp if last_message else ''
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
            return 'http://192.168.0.158:8081/home-delivery/img/logo.d251277d.svg'
        else: 
            return 'http://192.168.0.158:8081/home-delivery/img/logo.d251277d.svg'
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
