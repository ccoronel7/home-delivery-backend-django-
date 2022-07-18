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
router.register(r'order', views.OrderVS, basename='order')
router.register(r'order-details', views.OrderDetailVS, basename='order_details')
# Patterns
urlpatterns = [
    # Base
    path('', include(router.urls)),
    path('verificar-perfil', views.verificar_perfil),
    path('update-unread/', views.update_unread),
    path('order-create', views.order_create),
    path('order-update-deliver', views.order_update_deliver),
    path('order-update-cancel', views.order_update_cancel),
    path('order-update-statu', views.order_update_statu),
    path('pending-orders-client-side', views.pending_orders_client_side),
]

json = {
    "client": 1,
    "seller": 2,
    "delivery": 3,
    "pay_method": 1,
    "total_price": 3.2,
    "details": [
        {
            "contract_id": 1,
            "name": "Arroz con pollo",
            "category": ["Arroces","Platos caliente","Pollo"],
            "price": 3
        }
    ]
}
update_deliver = {
    "id":13,
    "delivery":3
}
update_deliver = {
    "id":13,
    "delivery":3
}
update_statu = {
    "id":13,
    "statu":"P"
}