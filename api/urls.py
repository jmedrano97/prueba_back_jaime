from django.urls import path
from .views import OrdenView,DireccionView

urlpatterns = [
    path('orden/',OrdenView.as_view(),name='ordenes_list'),
    path('orden/<int:id>',OrdenView.as_view(),name='orden_process'),
    path('direccion/',DireccionView.as_view(),name='direcciones'),
    path('direccion/<int:id>',DireccionView.as_view(),name='direcciones_process'),
]