"""
url de la aplicacion
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import SaleCreateView, SaleInvoicePdfView

urlpatterns = [
    path('pagprincipal/', views.restaurante, name="inicio"),
    path('sale/', SaleCreateView.as_view(), name="sale_create"),
    path('consultar_categoria/', views.consultar_categoria, name="consultar_categoria"),
    path('crear_categoria/', views.crear_categoria, name="crear_categoria"),
    path('editar_categoria<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('eliminar_categoria<int:id>/', views.eliminar_categoria, name="eliminar_categoria"),
    path('consultar_restaurante/', views.consultar_restaurante, name="consultar_restaurante"),
    path('crear_restaurante/', views.crear_restaurante, name="crear_restaurante"),
    path('editar_restaurante/<int:id>', views.editar_restaurante, name="editar_restaurante"),
    path('eliminar_restaurante/<int:id>', views.eliminar_restaurante, name="eliminar_restaurante"),
    path('consultar_producto/', views.consultar_producto, name="consultar_producto"),
    path('crear_producto/', views.crear_producto, name="crear_producto"),
    path('editar_producto<int:id>/', views.editar_producto, name="editar_producto"),
    path('eliminar_producto<int:id>/', views.eliminar_producto, name="eliminar_producto"),
    #path('consultar_pedido/', views.consultar_pedido, name="consultar_pedido"),
    #path('crear_pedido/', views.crear_pedido, name="crear_pedido"),
    path('consultar_empresa/', views.consultar_empresa, name="consultar_empresa"),
    path('crear_empresa/', views.crear_empresa, name="crear_empresa"),
    path('editar_empresa<int:id>/', views.editar_empresa, name="editar_empresa"),
    path('eliminar_empresa<int:id>/', views.eliminar_empresa, name="eliminar_empresa"),
    path('consultar_chofer/', views.consultar_chofer, name="consultar_chofer"),
    path('crear_chofer/', views.crear_chofer, name="crear_chofer"),
    path('editar_chofer<int:id>/', views.editar_chofer, name="editar_chofer"),
    path('eliminar_chofer<int:id>/', views.eliminar_chofer, name="eliminar_chofer"),
    path('consultar_zona/', views.consultar_zona, name="consultar_zona"),
    path('crear_zona/', views.crear_zona, name="crear_zona"),
    path('editar_zona<int:id>/', views.editar_zona, name="editar_zona"),
    path('eliminar_zona<int:id>/', views.eliminar_zona, name="eliminar_zona"),
    path('consultar_vehiculo/', views.consultar_vehiculo, name="consultar_vehiculo"),
    path('crear_vehiculo/', views.crear_vehiculo, name="crear_vehiculo"),
    path('editar_vehiculo<int:id>/', views.editar_vehiculo, name="editar_vehiculo"),
    path('eliminar_vehiculo<int:id>/', views.eliminar_vehiculo, name="eliminar_vehiculo"),
    path('consultar_factura/', views.consultar_factura, name="consultar_factura"),
    path('editar_factura<int:id>/', views.editar_factura, name="editar_factura"),
    path('salepdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
]