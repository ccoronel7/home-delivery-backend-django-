# Importes requeridos para urls del backend (api)
from rest_framework import routers
from django.urls import include, path
# Raiz
from . import views
# Router
router = routers.DefaultRouter()
# Utilidades
router.register(r'perfiles', views.PerfilVS, basename='perfil')
router.register(r'delivers', views.DeliverVS, basename='deliver')
router.register(r'chats', views.ChatVS, basename='chat')
router.register(r'mensajes', views.MensajeVS, basename='mensaje')
# Patterns
urlpatterns = [
    # Base
    path('', include(router.urls)),
    path('verificar-perfil', views.verificar_perfil),
    # path('', include(router.urls)),
]