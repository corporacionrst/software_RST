
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path = ws_scheme + '://' + window.location.host + '/cliente';
console.log("Conectando a " + ws_path);

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
        modal.style.display = "none";
	} else{
		alert("este proveedor ya existe");
		msn.attr("class", "alert alert alert-danger alert-dismissable");

	}
	document.getElementById("id_nit").value=data.nit;
	document.getElementById("id_nombre").value=data.nombre;
	document.getElementById("id_direccion").value=data.direccion;
	if (data.credito=="F"){
		$('#id_credito').prop('checked', false);
		document.getElementById("id_credito").enabled=false;
	}else{
		document.getElementById("id_credito").enabled=true;
	}

	$("#message").text(data.mensaje);
	msn.append(appended);
}
$("#proveedorForm").on("submit", function(event) {
	var mar=document.getElementById('id_monto_a_registrar').value;
	if (mar.split('.').length<=2){
	    var message = {
	        action: "crear_cliente",
	        nit:document.getElementById('id_nit_a_registrar').value,
			nombre:document.getElementById('id_nombre_a_registrar').value,
			dirs:document.getElementById('id_direccion_a_registrar').value,
			tel:document.getElementById('id_telefono_a_registrar').value,
			mail:document.getElementById('id_correo_a_registrar').value,
			comm:document.getElementById('id_comentario').value,
			credit:$('#id_es_set').is(":checked"),
			days:document.getElementById('id_dias_de_credito_a_registrar').value,
			money:mar,
			store:document.getElementById('tienda').value,  
	    };
	    socket.send(JSON.stringify(message));
   		$("#consultor_check").val('').focus();
	}else{
		alert("el monto no es valido");
	}
    return false;
});

if (socket.readyState == WebSocket.OPEN) socket.onopen();

