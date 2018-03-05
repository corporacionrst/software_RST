
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path = ws_scheme + '://' + window.location.host + '/marca';
// console.log("Conectando a " + ws_path)

socket = new WebSocket(ws_path);
socket.onmessage = function(e) {
	var msn =$("#message");
	$("#message").removeAttr("class");

	var data =JSON.parse(e.data);
	var appended = $("<a></a>").text("x");
	appended.attr("class","close");
	appended.attr("data-dismiss","alert");
	appended.attr("arial-label","close");

	if (data.exito=="SI"){
		msn.attr("class", "alert alert-success alert-dismissable");
	} else{
		msn.attr("class", "alert alert alert-danger alert-dismissable");

	}
	$("#message").text(data.mensaje);
	msn.append(appended);
}
$("#taskform").on("submit", function(event) {
	var ch=false
	try{ch = document.getElementById('id_importacion').checked;}
	catch(Exc){ch=false;}
    var message = {
        action: "crear_marca",
        nombre: document.getElementById('id_nombre').value,
        importacion:ch
    };
    socket.send(JSON.stringify(message));
    $("#id_importacion").val('').focus();
    return false;
});

// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();

