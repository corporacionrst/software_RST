
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path = ws_scheme + '://' + window.location.host + '/producto';
console.log("Conectando a " + ws_path)

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
		if(data.suma=="SI"){
			suma();
		}
	} else{
		msn.attr("class", "alert alert alert-danger alert-dismissable");

	}
	$("#message").text(data.mensaje);
	msn.append(appended);
}
$("#taskform").on("submit", function(event) {
    var message = {
        action: "crear_producto",
        codigo: document.getElementById('id_codigo').value,
        descripcion:document.getElementById('id_descripcion').value,
        marca: $('#id_marca').find(":selected").text(),
        set:$('#id_es_set').is(":checked"),
        no_set:document.getElementById('store_Set').value,

    };
    socket.send(JSON.stringify(message));
    $("#id_importacion").val('').focus();
    // alert($('#id_marca').find(":selected").text());
    return false;
});

// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();

function suma () {
	$.ajax({
		url:"/productos/sumar_d3",
		type:"get",
		success:function(data){
			document.getElementById('store_Set').value=data;
			page_set(0);
		}
	});

}
