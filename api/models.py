from django.db import models
from datetime import datetime
# Create your models here.

class Direccion(models.Model):
    CLIENTE   = 1
    TIENDA  = 2
    PUNTO  = 3
    TIPO = (
        (CLIENTE,'CLIENTE'),
        (TIENDA,'TIENDA'),
        (PUNTO,'PUNTO'),
    )
    nombre      = models.CharField(max_length=255)   
    coordenadas = models.CharField(max_length=255) 
    direccion   = models.CharField(max_length=255)
    numero_ext  = models.CharField(max_length=255)
    numero_int  = models.CharField(max_length=255, null=True)
    cp          = models.IntegerField(null=False)
    tipo        = models.IntegerField(choices=TIPO)
    def __str__(self):
        return '%s - %s'%(str(self.id),str(self.nombre))


class Orden(models.Model):
    CREADO      = 0
    RECOLECTADO = 1
    EN_ESTACION = 2
    EN_RUTA     = 3
    ENTREGADO   = 4
    CANCELADO   = 5
    ESTATUS = (
        (CREADO,'CREADO'),
        (RECOLECTADO,'RECOLECTADO'),
        (EN_ESTACION,'EN_ESTACION'),
        (EN_RUTA,'EN_RUTA'),
        (ENTREGADO,'ENTREGADO'),
        (CANCELADO,'CANCELADO'),
    )
    CHICO   = 1
    MEDIANO = 2
    GRANDE  = 3
    DEF     = 99
    PAQUETE = (
        (CHICO,'CHICO'),
        (MEDIANO,'MEDIANO'),
        (GRANDE,'GRANDE'),
        (DEF,'DEF'),
    )
    dirccion_origen    = models.ForeignKey(Direccion, related_name='ordenOrigen_Direccion',on_delete=models.CASCADE,blank=False,null=False)
    dirccion_destino   = models.ForeignKey(Direccion, related_name='ordenDestino_Direccion',on_delete=models.CASCADE,blank=False,null=False)
    cantidad_productos = models.IntegerField(null=False)
    peso_producutos    = models.IntegerField(null=False)
    estatus            = models.IntegerField(choices=ESTATUS)
    tipo_paquete       = models.IntegerField(choices=PAQUETE)
    fecha              = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

