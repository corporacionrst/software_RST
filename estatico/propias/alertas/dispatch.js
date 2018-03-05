
var ws_scheme_dispatch = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path_dispatch = ws_scheme_dispatch + '://' + window.location.host + '/despacho';
console.log("Conectando a " + ws_path_dispatch)
dispatch_socket = new WebSocket(ws_path_dispatch);

dispatch_socket.onmessage = function(e) {
	var data =JSON.parse(e.data);
	if(data.signal=="dispatchas"){
	$("#proceso").css({'background-color':'#F5F5F5', 'color': 'red'});
	$("#proceso").addClass('fa-3x');
	}

}

if (dispatch_socket.readyState == WebSocket.OPEN) dispatch_socket.onopen();
