
var ws_scheme_notify = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path_notify = ws_scheme_notify + '://' + window.location.host + '/notificaciones';
console.log("Conectando a " + ws_path_notify)
notify_socket = new WebSocket(ws_path_notify);

notify_socket.onmessage = function(e) {
	var data =JSON.parse(e.data);
	if (data.signal=="dropdown_productos"){
		$("#dropdown_productos").css({'background-color':'#F5F5F5', 'color': '#7FFF00'});
		$("#dropdown_productos").addClass('fa-3x');
	}

}

if (notify_socket.readyState == WebSocket.OPEN) notify_socket.onopen();
