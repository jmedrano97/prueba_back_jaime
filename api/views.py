from unittest import registerResult
from django.views import View
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from .models import *
import json
import time
# Create your views here.

class OrdenView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def get(self,request,id=0):
        if id>0:
            ordenes= list(Orden.objects.filter(id=id).values())
            if len(ordenes)>0:
                orden = ordenes[0]
                datos = {'mensaje': 'Success','orden':orden}
            else:
                datos = {'mensaje': 'Sin orden'}
        else:
            ordenes= list(Orden.objects.values())
            if len(ordenes)>0:
                datos = {'mensaje': 'Success','ordenes':ordenes}
            else:
                datos = {'mensaje': 'No se ha encontrado la orden'}

        return JsonResponse(datos)
    
    def post(self,request):
        entrada = json.loads(request.body)
        cantidad=entrada['cantidad_productos']
        peso = entrada['peso_producutos']
        datos_correctos = validacion(cantidad,peso)
        if datos_correctos:
            tipo=obtener_tam(peso)
            if tipo > 0:
                estatus=Orden.CREADO
                Orden.objects.create(
                    cantidad_productos=cantidad,
                    peso_producutos=peso,
                    estatus=estatus,
                    tipo_paquete=tipo
                )
                datos={'mensaje':'Orden creada'}
            else:
                datos={'mensaje':'NOTA: No contamos con el servicio estándar para el tipo de paquete. Por favor comuníquese con la empresa para realizar un convenio especial.'}
        else:
            datos={'mensaje':'Error en los datos.'}

        return JsonResponse(datos)

    def put(self,request, id):
        entrada = json.loads(request.body)
        ordenes = list(Orden.objects.filter(id=id).values())
        if len(ordenes)>0:
            orden = Orden.objects.get(id=id)
            if entrada['estatus'] == 5:
                estatus_actual= orden.estatus
                if estatus_actual==Orden.EN_RUTA or estatus_actual==Orden.ENTREGADO:
                    datos = {'mensaje': 'La orden ya no puede ser cancelada. Estado: %s.'%orden.estatus}
                else:
                    creacion=orden.fecha.replace(tzinfo=None)
                    actual=datetime.now()
                    delta = timedelta(
                        minutes=2,
                    )
                    total=actual-creacion
                    orden.estatus = Orden.CANCELADO
                    orden.save()

                    if total <= delta:
                        datos = {'mensaje': 'Orden cancelada. Se ha realizado el reembolso'}
                    else:
                        datos = {'mensaje': 'Orden cancelada. El reembolso solo aplica cuando una orden es cancelada dentro de los primeros 2 minutos, tu orden fue creada hace: %s'%total}
            else:
                orden.estatus = entrada['estatus']
                orden.save()
                datos = {'mensaje': 'Se cambio el estatus de la orden. Estatus: %s'%entrada['estatus']}
        else:
            datos = {'mensaje': 'No se ha encontrado la orden'}
        return JsonResponse(datos)

def validacion(cantidad,peso):
    if cantidad>0 and peso>0:
        return True
    else:
        return False

def obtener_tam(peso):
    if peso >0 and peso<=5:
        respuesta = Orden.CHICO
    elif peso > 5 and peso <= 15:
        respuesta = Orden.MEDIANO
    elif peso >15 and peso <= 25:
        respuesta = Orden.GRANDE
    elif peso > 25:
        respuesta = 0
    return respuesta
