from pydoc import describe
from pyexpat import model
from tkinter import CASCADE
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
