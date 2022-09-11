from django.db import models
from datetime import datetime
# Create your models here.
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
    cantidad_productos = models.IntegerField(null=False)
    peso_producutos = models.IntegerField(null=False)
    estatus = models.IntegerField(choices=ESTATUS)
    tipo_paquete       = models.IntegerField(choices=PAQUETE)
    fecha              = models.DateTimeField(auto_now_add=True)