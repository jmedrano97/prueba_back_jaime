from django.contrib import admin
from .models import Orden,Direccion
# Register your models here.
# admin.site.register(Orden)
# admin.site.register(Direccion)

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display       = ('id','nombre','tipo','coordenadas')
    search_fields      = ['id','nombre']
    list_display_links = ('id','nombre')

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display       = ('id','cantidad_productos','peso_producutos','estatus','tipo_paquete')
    search_fields      = ['id']