from django.urls import path
from .views import OrdenView

urlpatterns = [
    path('orden/',OrdenView.as_view(),name='ordenes_list'),
    path('orden/<int:id>',OrdenView.as_view(),name='orden_process')
]