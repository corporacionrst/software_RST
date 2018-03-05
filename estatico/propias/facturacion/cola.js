function refresh () {
	window.location.reload();
}
function rechazar_doc (id) {
	var motivo = prompt("Motivo por el cual se rechazo", "");
	if (motivo == "" ) {
		alert("por favor ingrese el motivo");
		rechazar_doc(id);
	} else if(motivo!=null){
	    var message={
            action:"rechazar_impresion",
            documento:id,
            motivo:motivo,
        };
        alert_socket.send(JSON.stringify(message));
	    alert("el usuario ha sido notificado");
		window.location.reload()
	}
}


function mostrar (data) {
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'>"
	html+="<tr><th>i</th><th>nit</th><th>nombre</th><th>total</th><th>rechazar</th><th>imprimir</th><th>cobrar</th></tr>";
	for(i=0;i<data.length;i++){
		html+="<tr><td>";
		var indice=i+1
		var total=(data[i].lista__descuento>0)?data[i].lista__descuento:data[i].lista__total;
		html+=indice+"</td><td>"+data[i].cliente_proveedor__nit+"</td><td>"+data[i].cliente_proveedor__nombre+"</td><td>"+total+"</td><td><button class='btn-lg btn-danger' onclick='rechazar_doc("+data[i].id+")'><i class='fa fa-trash' aria-hidden='true'></i></button></td><td><button class='btn-lg btn-success' onclick='imprimir_documento("+data[i].id+")'><i class='fa fa-print' aria-hidden='true'></i></button></td><td><button class='btn-lg btn-primary' onclick='cobrar_documento("+data[i].id+")'><i class='fa fa-thumbs-up' aria-hidden='true'></i></button></td>"
		"</td></tr>"
	}
	return html;
}
function contado (pag) {
	$.ajax({
		data:{"pag":pag},
		url:"/caja/contado",
		type:"get",
		success:function(data){
			$("#tabla_contado").html(mostrar(data));
		}
	})
}

function credito(pag){
	$.ajax({
		data:{"pag":pag},
		url:"/caja/credito",
		type:"get",
		success:function(data){
			$("#tabla_credito").html(mostrar(data));
		}
	})
}

function salta(id){
	window.location.reload();
}
function imprimir_documento (id) {
	var serie = document.getElementById('ddl_serie').value;
	if (serie==null || serie==""){
		alert("no tienes ninguna serie asignada");
	}else{
		$.ajax({
			data:{
				"documento":id,
				"serie":serie,
				"csrfmiddlewaretoken":mitoken
			},
			url:"/caja/imprimir/",
			type:"post",
			success:function (data) {
				alert(data)
				window.location.reload();
			}
		});
		var brchwin = window.open(id, 'branch', 'width=1000,height=1000,status=no,resizable=yes,scrollbars=yes');
	}
}

  	


function almacenar(valor,correo){
	$.ajax({
		data:{
		"id":valor,
		"correo":correo,
		},
		url:"",
		type:"get",
		success:function (data) {
			imprimir(id);

		}

	})
	

}

function imprimir(id){

}


$(document).ready(function(){
	contado(0);
	credito(0);
});
