from pyexpat import model
from statistics import mode
from django.db import models
from django.forms import IntegerField
class Perfil(models.Model):
    wallet=models.TextField(null=False,blank=False)
    nombre=models.CharField(max_length=32,null=False,blank=False)
    imagen=models.ImageField(upload_to='perfiles',null=True)
    delivery=models.BooleanField(default=False)
    vendedor=models.BooleanField(default=False)
    telefono=models.CharField(max_length=32,null=False,blank=True,default='')
    direccion=models.TextField(null=False,blank=True,default='')
    location=models.TextField(null=False,blank=True,default='')
    def __str__(self):
        tipo='Delivery' if self.delivery else 'Usuario'
        tipo='Vendedor' if self.vendedor else tipo
        return '%s/%s (%s)'%(self.nombre,tipo,self.id)
class Deliver(models.Model):
    perfil=models.ForeignKey(Perfil,null=False,on_delete=models.CASCADE)
    TIPOS=(('A','Automovil'),('M','Moto'),('B','Bicicleta'))
    tipo=models.CharField(max_length=1,choices=TIPOS,null=False,blank=False)
    v_marca=models.CharField(max_length=32,null=False,blank=False)
    v_modelo=models.CharField(max_length=32,null=False,blank=False)
    v_color=models.CharField(max_length=16,null=False,blank=False)
    v_placa=models.CharField(max_length=32,null=False,blank=False)
    activo = models.BooleanField(default=False)
    def save(self):
        super().save()
        if self.id:
            usuario=Perfil.objects.get(id=self.perfil.id)
            usuario.delivery=True
            usuario.save()
    def __str__(self):
        return '%s/Vehiculo (%s)'%(self.perfil.nombre,self.id)
class Chat(models.Model):
    usuarios=models.ManyToManyField(Perfil)
    roomName=models.CharField(max_length=32,null=False,blank=False)
    # unreadCount=models.IntegerField(null=False,default=0)
class Mensaje(models.Model):
    chat=models.ForeignKey(Chat,null=False,on_delete=models.DO_NOTHING)
    usuario=models.ForeignKey(Perfil,null=False,on_delete=models.DO_NOTHING)
    content=models.TextField(null=False,blank=False)
    # senderid=models.CharField()
    datetime=models.DateTimeField(auto_now_add=True)
    system=models.BooleanField(default=False)
    saved=models.BooleanField(default=True)
    distributed=models.BooleanField(default=False)
    seen=models.BooleanField(default=False)
    deleted=models.BooleanField(default=False)
    # failure=models.BooleanField(default=False)
    disableActions=models.BooleanField(default=True)
    disableReactions=models.BooleanField(default=True)
    # files=models.CharField()
    # reactions=models.CharField()
    # replyMessage=models.ForeignKey()
    reply_to=models.ForeignKey('self',null=True,on_delete=models.CASCADE)
    def __str__(self):
        return '%s (%s)'%(self.content,self.usuario.nombre)
# class Reacciones(models.Model):
#     mensaje=models.ForeignKey(Mensajes,null=False,blank=False)
#     usuario=models.ForeignKey(Perfil,null=False,blank=False)
#     reaccion=models.CharField(max_length=254,null=False,blank=False)
class ArchivoMensaje(models.Model):
    name=models.CharField(max_length=32,null=False,blank=False)
    size=models.IntegerField(null=False,blank=False,default=19600)
    tipo=models.CharField(max_length=5,null=False,blank=False,default='png')
    # audio=models.BooleanField()
    # duration=models.
    url=models.ImageField(upload_to='mensajes',null=False)
    # preview=models.URLField()

class PayMethod(models.Model):
    name=models.TextField(null=False)
    def __str__(self):
        return '%s'%(self.name)

class Order(models.Model):
    # Client
    client=models.ForeignKey(Perfil,null=True,on_delete=models.SET_NULL,related_name='profile_client')
    client_data=models.TextField(null=False)
    client_location = models.TextField(null=False)
    direccion = models.TextField(null=False)
    # Seller
    seller=models.ForeignKey(Perfil,null=True,on_delete=models.SET_NULL,related_name='profile_seller')
    seller_data=models.TextField(null=False,blank=True)
    seller_location = models.TextField(null=False)
    name_shop = models.TextField(null=False,blank=True)
    wallet_shop = models.TextField(null=False,blank=True)
    # Deliver
    delivery=models.ForeignKey(Perfil,null=True,on_delete=models.SET_NULL,related_name='profile_delivery')
    delivery_data=models.TextField(null=True)
    possible=models.ManyToManyField(Perfil, blank=True)
    # Metodo pago
    pay_method=models.ForeignKey(PayMethod,null=True,on_delete=models.SET_NULL)
    pay_method_data=models.TextField(null=True)
    # Costo
    deliver_cost=models.FloatField(default=0)
    total_price=models.FloatField(default=0)
    chat = models.ForeignKey(Chat,on_delete=models.DO_NOTHING)
    # Estado
    STATUS=(('R','En revision'),('N','Pendiente'),('P','Preparando'),('C','En camino'),('E','Entregado'),('B','Recibido'),('X','Cancelado'))
    statu=models.CharField(max_length=1,choices=STATUS,null=False,blank=False,default='R')
    raison_cancel = models.TextField(default='')
    def __str__(self):
        return '#%s (Client: %s, Seller: %s, Deliver: %s)'%(self.id,self.client.id,self.seller.id,self.delivery.id if self.delivery else 'Ninguno')

class OrderDetail(models.Model):
    order=models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
    # contract_id=models.IntegerField(null=False)
    name=models.TextField(null=False)
    # category=models.TextField(null=False)
    price=models.FloatField(null=False)
    comment= models.TextField(null=True)
    def __str__(self):
        return '#%s (%s,%s)'%(self.id,self.order.id,self.name)

json = {
    'client': 1, # Id del usuario delivery
    'seller': 2, # Id del usuario delivery
    'delivery': 3, # Id del usuario delivery
    'pay_method': 1, # Metodo de pago (Near,Usdt,Usd,Busd,BsS,etc)
    'total_price': 3.2, # Precio total de los detalles mas comision del Deliery
    'details': [
        {
            'contract_id': 1, # id en el contrato
            'name': 'Arroz con pollo', # Nombre en el contrato
            'category': '["Arroces","Platos caliente", "Pollo"]', # Categorias asociadas en el contrato
            'price': 3 # Precio obtenido del contrato
        }
    ]
}
json = {
    'perfil':1, # Id del perfil en el backend
    'tipo':'A', # Tipos: ('A','Automovil'),('M','Moto'),('B','Bicicleta')
    'v_marca':'Toyota', # texto
    'v_modelo':'Modelo X', # texto
    'v_color':'Negro', # Texto
    'v_placa':'3POI16', # texto
}