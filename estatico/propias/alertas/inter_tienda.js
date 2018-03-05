
var ws_scheme_inter_tienda = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path_inter_tienda = ws_scheme_inter_tienda + '://' + window.location.host + '/inter_tiendaas';
console.log("Conectando a " + ws_path_inter_tienda)
inter_tienda_socket = new WebSocket(ws_path_inter_tienda);

inter_tienda_socket.onmessage = function(e) {
	var data =JSON.parse(e.data);
	if (data.usuario==usuario){
		var html=""
		html+="__Solicitud de traslad<i class='fa fa-cog fa-1 fa-spin' aria-hidden='true'></i>!!";
		$("#traslados_pendientes_de_autorizar").html(html);
	}
}
if (inter_tienda_socket.readyState == WebSocket.OPEN) inter_tienda_socket.onopen();
