from unittest import registerResult
from django.views import View
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from django.shortcuts import get_object_or_404
from .models import *
import xlrd
import json
import time
TOKEN_CLIENTE = 'token_cliente_1234'
TOKEN_INTERNO = 'token_interno_123'
# Create your views here.

class OrdenView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def get(self,request,id=0):
        try:
            token_rq = request.headers['Token']
            if(token_rq==TOKEN_CLIENTE or token_rq==TOKEN_INTERNO):
                if id>0:
                    obj_ordenes= Orden.objects.filter(id=id)
                    ls_ordenes = obj_segmentado(obj_ordenes)
                    if len(ls_ordenes)>0:
                        orden = ls_ordenes[0]
                        datos = {'mensaje': 'Éxito','orden':orden}
                    else:
                        datos = {'mensaje': 'Sin orden'}
                else:
                    if(token_rq==TOKEN_INTERNO):
                        obj_ordenes = Orden.objects.all()
                        ls_ordenes = obj_segmentado(obj_ordenes)
                        if len(ls_ordenes)>0:
                            datos = {'mensaje': 'Éxito','ordenes':ls_ordenes}
                        else:
                            datos = {'mensaje': 'No se ha encontrado la orden'}
                    else:
                        datos = {'mensaje': 'Token no valido'}
            else:
                datos = {'mensaje': 'Token no valido'}
        except Exception as e:
            print(str(e))
            datos={'mensaje':'Error: %s.'%e}
        return JsonResponse(datos)
    
    def post(self,request,file=''):
        try:
            mensaje=''
            id_creado=''
            orden_actual=''
            ids_ls=[]
            ordenes_ls=[]
            token_rq = request.headers['Token']
            if(token_rq==TOKEN_CLIENTE or token_rq==TOKEN_INTERNO):
                #File es una variable que se obtiene de la url
                if file == 'Subir_archivo':  #Si se obtiene Subir_archivo realiza el procedieminto con xls
                    ls_file=[]
                    archivo = ('formato_post.xls') #Se ingresa la ruta (en este caso en la carpeta raiz)
                    openArchivo = xlrd.open_workbook(archivo) 
                    sheet = openArchivo.sheet_by_name('Sheet1')
                    #Cuando se trae los datos del archivo recorre las filas
                    for i in range(sheet.nrows):
                        i+1
                        #Se agregan a un diccionario con las mismas llaves que el post
                        dic_file={
                            "dirccion_origen_id": (sheet.cell_value(i,0)),
                            "dirccion_destino_id": (sheet.cell_value(i,1)),
                            "cantidad_productos": (sheet.cell_value(i,2)),
                            "peso_producutos": (sheet.cell_value(i,3))
                        }
                        ls_file.append(dic_file) #el diccionario se agrega una lista
                    entrada= ls_file #esta lista se va a recorrer en el procedimiento que ya se hacia antes
                else:
                    #Si no es Subir_archivo se extraen los datos del body como ya se hacia normalmente
                    entrada = json.loads(request.body)
                    entrada= [entrada]

                for i in entrada:
                    #Aquí empieza el funcionamiento original
                    origen  =i['dirccion_origen_id']
                    cantidad=i['dirccion_destino_id']
                    origen_obj = get_object_or_404(Direccion, pk=origen)
                    cantidad_obj = get_object_or_404(Direccion, pk=cantidad)
                    cantidad=i['cantidad_productos']
                    peso = i['peso_producutos']
                    datos_correctos = validacion(cantidad,peso)
                    if datos_correctos:
                        tipo=obtener_tam(peso)
                        if tipo > 0:
                            estatus=Orden.CREADO
                            actual_creada=Orden.objects.create(
                                dirccion_origen=origen_obj,
                                dirccion_destino=cantidad_obj,
                                cantidad_productos=cantidad,
                                peso_producutos=peso,
                                estatus=estatus,
                                tipo_paquete=tipo
                            )
                            orden_actual = unico_segmentado(actual_creada)
                            mensaje='Éxito'
                            id_creado=actual_creada.id
                            ids_ls.append(id_creado)
                            ordenes_ls.append(orden_actual)
                        else:
                            if(token_rq==TOKEN_INTERNO):
                                estatus=Orden.CREADO
                                actual_creada=Orden.objects.create(
                                    dirccion_origen=origen_obj,
                                    dirccion_destino=cantidad_obj,
                                    cantidad_productos=cantidad,
                                    peso_producutos=peso,
                                    estatus=estatus,
                                    tipo_paquete=tipo
                                )
                                orden_actual = unico_segmentado(actual_creada)
                                mensaje='Éxito'
                                id_creado=actual_creada.id
                                ids_ls.append(id_creado)
                                ordenes_ls.append(orden_actual)
                            else:
                                mensaje='NOTA: No contamos con el servicio estándar para el tipo de paquete. Por favor comuníquese con la empresa para realizar un convenio especial.'
                    else:
                        mensaje='Error en los datos.'
                    
                    datos={'mensaje':mensaje,'id_creado':ids_ls,'orden_actual':ordenes_ls}
            else:
                datos = {'mensaje': 'Token no valido'}
        except Exception as e:
            print(str(e))
            datos={'mensaje':'Error: %s.'%e}
        # datos={'mensaje':'Prueba'}
        return JsonResponse(datos)

    def put(self,request, id):
        try:
            token_rq = request.headers['Token']
            if(token_rq==TOKEN_CLIENTE or token_rq==TOKEN_INTERNO):
                entrada = json.loads(request.body)
                ordenes = list(Orden.objects.filter(id=id).values())
                if len(ordenes)>0:
                    orden = Orden.objects.get(id=id)
                    if entrada['estatus'] == Orden.CANCELADO:
                        estatus_actual= orden.estatus
                        if estatus_actual==Orden.EN_RUTA or estatus_actual==Orden.ENTREGADO:
                            datos = {'mensaje': 'La orden ya no puede ser cancelada. Estatus: %s.'%Orden.ESTATUS[orden.estatus][1]}
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
                        if(token_rq==TOKEN_INTERNO):
                            orden.estatus = entrada['estatus']
                            orden.save()
                            orden_nueva = unico_segmentado(orden)
                            datos = {'mensaje': 'Se cambio el estatus de la orden. Estatus: %s'%Orden.ESTATUS[orden.estatus][1],'orden_actual':orden_nueva}
                        else:
                            datos = {'mensaje': 'Token no valido'}
                else:
                    datos = {'mensaje': 'No se ha encontrado la orden'}
            else:
                datos = {'mensaje': 'Token no valido'}
        except Exception as e:
            print(str(e))
            datos={'mensaje':'Error: %s.'%e}
        return JsonResponse(datos)

    def delete(self,request):
        try:
            token_rq = request.headers['Token']
            if(token_rq==TOKEN_INTERNO):
                print('Estoy en delete')
                ordenes = Orden.objects.filter(estatus=5)
                print('ordenes: ',ordenes)
                if len(ordenes)>0:
                    for i in ordenes:
                        i.delete()
                    datos = {'mensaje': 'Las ordenes canceladas han sido borradas con exito.'}
                else:
                    datos = {'mensaje': 'No existen ordenes cancelas para borrar.'}
            else:
                datos = {'mensaje': 'Token no valido'}
        except Exception as e:
            print(str(e))
            datos={'mensaje':'Error: %s'%e}
        return JsonResponse(datos)

class DireccionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def get(self,request,id=0):
        try:
            if id>0:
                direcciones= list(Direccion.objects.filter(id=id).values())
                if len(direcciones)>0:
                    direccion = direcciones[0]
                    datos = {'mensaje': 'Éxito','direccion':direccion}
                else:
                    datos = {'mensaje': 'Sin orden'}
            else:
                direcciones= list(Direccion.objects.values())
                if len(direcciones)>0:
                    datos = {'mensaje': 'Éxito','direcciones':direcciones}
                else:
                    datos = {'mensaje': 'Error 404'}
        except Exception as e:
            print(str(e))
            datos={'mensaje':'Error: %s.'%e}

        return JsonResponse(datos)
    
    def post(self,request):
        try:
            entrada = json.loads(request.body)
            nombre      = entrada['nombre']
            coordenadas = entrada['coordenadas']
            direccion   = entrada['dirrecion']
            numero_ext  = entrada['numero_ext']
            numero_int  = entrada['numero_int']
            cp          = entrada['cp']
            tipo        = entrada['tipo']
            actual_creada= Direccion.objects.create(
                nombre=nombre,
                coordenadas=coordenadas,
                direccion=direccion,
                numero_ext=numero_ext,
                numero_int=numero_int,
                cp=cp,
                tipo=tipo
            )
            datos={'mensaje':'Dirección creada: %s'%nombre, 'id_creado':actual_creada.id}
        except Exception as e:
            print(str(e))
            datos={'mensaje':'Error: %s.'%e}
        return JsonResponse(datos)

    def put(self,request, id):
        try:
            entrada = json.loads(request.body)
            direcciones = list(Direccion.objects.filter(id=id).values())
            if len(direcciones)>0:
                direccion = Direccion.objects.get(id=id)
                direccion.nombre      = entrada['nombre']
                direccion.coordenadas = entrada['coordenadas']
                direccion.direccion   = entrada['direccion']
                direccion.numero_ext  = entrada['numero_ext']
                direccion.numero_int  = entrada['numero_int']
                direccion.cp          = entrada['cp']
                direccion.tipo        = entrada['tipo']
                direccion.save()
                
                datos = {'mensaje': 'Dirección modificada','id_actual':direccion.id}
            else:
                datos = {'mensaje': 'No se ha encontrado la orden'}
        except Exception as e:
            print(str(e))
            datos={'mensaje':'Error: %s'%e}
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


def obj_segmentado(obj_ordenes):
    ls_dic=[]
    for i in obj_ordenes:
        dic={}
        dic["id"]=i.id          
        dic["dirccion_origen_id"]=i.dirccion_origen_id          
        dic["dirccion_origen_nombre"]=i.dirccion_origen.nombre     
        dic["dirccion_destino_id"]=i.dirccion_destino_id            
        dic["dirccion_destino_nombre"]=i.dirccion_destino.nombre            
        dic["cantidad_productos"]=i.cantidad_productos          
        dic["peso_producutos"]=i.peso_producutos            
        dic["estatus"]=i.estatus            
        dic["estatus_nombre"]=Orden.ESTATUS[i.estatus][1]             
        dic["tipo_paquete"]=i.tipo_paquete          
        dic["fecha"]=i.fecha            
        ls_dic.append(dic)
    return(ls_dic)

def unico_segmentado(obj_ordenes):
    ls_dic=[]
    dic={}
    dic["id"]=obj_ordenes.id          
    dic["dirccion_origen_id"]=obj_ordenes.dirccion_origen_id          
    dic["dirccion_origen_nombre"]=obj_ordenes.dirccion_origen.nombre     
    dic["dirccion_destino_id"]=obj_ordenes.dirccion_destino_id            
    dic["dirccion_destino_nombre"]=obj_ordenes.dirccion_destino.nombre            
    dic["cantidad_productos"]=obj_ordenes.cantidad_productos          
    dic["peso_producutos"]=obj_ordenes.peso_producutos            
    dic["estatus"]=obj_ordenes.estatus  
    dic["estatus_nombre"]=Orden.ESTATUS[obj_ordenes.estatus][1]             
    dic["tipo_paquete"]=obj_ordenes.tipo_paquete          
    dic["fecha"]=obj_ordenes.fecha            
    ls_dic.append(dic)
    return(ls_dic)