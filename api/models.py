from django.db import models

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
    cantidad_productos = models.IntegerField(null=False)
    peso_prodcutos = models.IntegerField(null=False)
    estatus = models.IntegerField(choices=ESTATUS)