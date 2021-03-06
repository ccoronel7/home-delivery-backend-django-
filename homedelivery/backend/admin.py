from django.contrib import admin
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
from .models import *
# Registrar
admin.site.register(Perfil)
admin.site.register(Deliver)
admin.site.register(Chat)
admin.site.register(Mensaje)
admin.site.register(PayMethod)
admin.site.register(Order)
admin.site.register(OrderDetail)
# Eliminar del admin
admin.site.unregister(Group)
admin.site.unregister(User)