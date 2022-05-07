from django.contrib import admin
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
from .models import *
# Registrar
admin.site.register(Perfil)
admin.site.register(Deliver)
# Eliminar del admin
admin.site.unregister(Group)
admin.site.unregister(User)