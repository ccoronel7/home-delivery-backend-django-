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
router.register(r'tiendas', views.TiendaVS, basename='tienda')
router.register(r'categorias', views.CategoriaVS, basename='categoria')
router.register(r'productos', views.ProductoVS, basename='producto')
router.register(r'detalles-productos', views.DetalleProductoVS, basename='detalleproducto')
# Patterns
urlpatterns = [
    # Base
    path('', include(router.urls)),
    path('verificar-perfil', views.verificar_perfil),
    path('prueba', views.prueba),
    # path('', include(router.urls)),
]