
var ws_scheme_dispatch = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path_dispatch = ws_scheme_dispatch + '://' + window.location.host + '/cola';
console.log("Conectando a " + ws_path_dispatch)
cola_socket = new WebSocket(ws_path_dispatch);

cola_socket.onmessage = function(e) {
	var data =JSON.parse(e.data);
	if (data.tienda==tienda){
		tabla(data);
	}
}

if (cola_socket.readyState == WebSocket.OPEN) cola_socket.onopen();




function registrar_venta(){
	var nit=document.getElementById("id_nit").value;
	var credito=document.getElementById("id_credito").checked;
	if (nit==""){
		alert("por favor ingrese el nit del cliente");

	}else{cargar_documento(nit,credito);
	}
	
}

function cargar_documento (nit,credito){
	$.ajax({
		data:{
			"nit":nit,
			"credito":credito,
			"pagina":page_id
		},
		url:"/clientes/mayorista",
		type:"get",
		success:function(data){
			if (data.includes("MAYORISTA")){
				if (confirm(data)){
					aplicar_descuento();
				}else{
					venta();

				}
			}else if(data.includes("PERMISO")){
				if (confirm(data)){
					pedir_permiso(nit);
				}
			}else if(data.includes("NO")){
				alert(data);
				return
			}
			else{
				venta("documento en caja");
			}

		}
	});

}


function aplicar_descuento () {
	$.ajax({
		data:{
			"pag":page_id,
			"csrfmiddlewaretoken":mitoken
		},
		url:"/clientes/descuento/",
		type:"POST",
		success:function (data) {
			alert(data);
			venta("APLICADO: documento en caja");
		}

	});
}
function pedir_permiso(nit){
	var message={
		"action":"pedir_permiso",
		"usuario":usuario,
	}
	alert_socket.send(JSON.stringify(message));
	venta("permiso solicitado")

}

function venta (mensaje) {
	var cola_producto={
		action:"agregar_productos",
		pagina:page_id,
		usu:usuario
	};
	cola_socket.send(JSON.stringify(cola_producto));
	alert(mensaje)
	a_caja();
	
	
}
function a_caja () {
	$.ajax({
		data:{
			"nit":document.getElementById('id_nit').value,
			"credito":document.getElementById("id_credito").checked,
			"pag":page_id,
			"csrfmiddlewaretoken":mitoken
		},
		url:"/facturar/",
		type:"POST",
		success:function(data){
			window.location.reload();
		}

	});
}

