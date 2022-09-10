from unittest import registerResult
from django.views import View
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
import json
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
                datos = {'mensaje': 'Sin ordenes'}

        return JsonResponse(datos)
    
    def post(self,request):
        entrada = json.loads(request.body)
        Orden.objects.create(
            cantidad_productos=entrada['cantidad_productos'],
            peso_prodcutos=entrada['peso_prodcutos'],
            estatus=entrada['estatus'])
        datos={'mensaje':'Success'}
        return JsonResponse(datos)

    def put(self,request, id):
        entrada = json.loads(request.body)
        ordenes = list(Orden.objects.filter(id=id).values())
        if len(ordenes)>0:
            orden = Orden.objects.get(id=id)
            orden.cantidad_productos = entrada['cantidad_productos']
            orden.peso_prodcutos = entrada['peso_prodcutos']
            orden.estatus = entrada['estatus']
            orden.save()
            datos = {'mensaje': 'Success'}
        else:
            datos = {'mensaje': 'Sin ordenes'}
        return JsonResponse(datos)
