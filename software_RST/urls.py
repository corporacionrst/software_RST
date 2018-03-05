from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include("app.sitio.urls",namespace="noticias")),
    url(r'^bodega/', include("app.sistema.bodega.bodega.urls",namespace="bodega")),
    url(r'^productos/', include("app.productos.producto.urls",namespace="producto")),
    url(r'^inventario/', include("app.productos.inventario.inventario.urls",namespace="inventario")),
    url(r'^tienda/', include("app.sistema.tienda.urls",namespace="tienda")),

    url(r'^caja/', include("app.sistema.cobros.caja.urls",namespace="cobros")),
    url(r'^conta/', include("app.sistema.conta.conta.urls",namespace="conta")),
    
    url(r'^clientes/', include("app.cliente_proveedor.cliente.urls",namespace="clientes")),
    url(r'^proveedores/', include("app.cliente_proveedor.proveedor.urls",namespace="proveedores")),
    
	url(r'^admin/', include("app.sistema.administrador.administrador.urls",namespace="administrador")),
    url(r'^alertas/', include("app.alertas.urls",namespace="alert_socket")),
    
    url(r'^facturar/', include("app.sistema.ventas.facturacion.urls",namespace="facturacion")),
    url(r'^imprimir/',include("app.imprimir.urls",namespace="imprimir")),
    url(r'^proforma/',include("app.proformas.urls",namespace="proforma")),
    
    
    url(r'^envios/',include("app.envios.urls",namespace="envios")),
    

    url(r'^admin_punto_php/', admin.site.urls), 
    url(r'^orden_de_compra/',include("app.productos.inventario.orden.urls",namespace="orden")),
    url(r'^historial/',include("app.productos.inventario.historial.urls",namespace="historial")),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
