from channels import include

channel_routing = [
	include("app.productos.marca.routing.websocket_routing",path=r'^/marca'),
	include("app.productos.producto.routing.websocket_routing",path=r'^/producto'),
	include("app.cliente_proveedor.proveedor.routing.websocket_routing",path=r'^/proveedor'),
	include("app.cliente_proveedor.cliente.routing.websocket_routing",path=r'^/cliente'),
	include("app.alertas.routing.websocket_routing",path=r'^/alertas'),
	include("app.sistema.bodega.traslados.routing.websocket_routing",path=r'^/inter_tiendaas'),
	include("app.imprimir.routing.websocket_routing",path=r'^/cola'),
	include("app.sistema.usuarios.routing.websocket_routing",path=r'^/salarios'),
]