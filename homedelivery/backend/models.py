from django.db import models
class Perfil(models.Model):
    wallet=models.TextField(null=False,blank=False)
    nombre=models.CharField(max_length=32,null=False,blank=False)
    imagen=models.ImageField(upload_to='perfiles',null=True)
    delivery=models.BooleanField(default=False)
    vendedor=models.BooleanField(default=False)
    telefono=models.CharField(max_length=32,null=False,blank=True,default='')
    direccion=models.TextField(null=False,blank=True,default='')
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
    unreadCount=models.IntegerField(null=False,blank=False,default=1)
class Mensaje(models.Model):
    chat=models.ForeignKey(Chat,null=False,on_delete=models.DO_NOTHING)
    usuario=models.ForeignKey(Perfil,null=False,on_delete=models.DO_NOTHING)
    content=models.TextField(null=False,blank=False)
    # senderid=models.CharField()
    date=models.TextField(null=False,blank=False)
    timestamp=models.CharField(max_length=5,null=False,blank=False)
    system=models.BooleanField(default=False)
    saved=models.BooleanField(default=False)
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
