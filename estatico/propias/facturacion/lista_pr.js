function cobrar_documento (argument) {
	alert(argument)
	// body...
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


function mostrar (data,pag) {
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'>"
	html+="<tr><th>no</th><th>vendedor</th><th>fecha de vencimiento</th><th>modificar</th><th>facturar</th></tr>";
	for(i=0;i<data.length;i++){
		html+="<tr><td>"+data[i].id+"</td><td>"+data[i].vendedor__usuario__username+"</td><td>"+data[i].fecha_vencimiento+"</td>"
		if (data[i].vendedor__usuario__id==usuario){
			html+="<td><button class='btn-lg btn-success' onclick='imprimir_documento("+data[i].id+")'><i class='fa fa-edit' aria-hidden='true'></i></button></td><td><button class='btn-lg btn-primary' onclick='cobrar_documento("+data[i].id+")'><i class='fa fa-print' aria-hidden='true'></i></button></td>"
		"</td></tr>"

		}else{
			html+="<td>X</td><td><button class='btn-lg btn-primary' onclick='cobrar_documento("+data[i].id+")'><i class='fa fa-print' aria-hidden='true'></i></button></td>"
		"</td></tr>"
		}

	}
	var prev="",next="";
	if (data.length==10){
		var sigue = pag+1
		next="<button class='btn' onclick='contado("+sigue+")'> -> </button>"
	}
	if (pag!=0){
		var fue = pag-1
		prev="<button class='btn' onclick='contado("+fue+")'> <- </button>"

	}
	html+="<tr><td colspan='3'></td><td>"+prev+"</td><td>"+next+"</td></tr>"

	return html;
}
function contado (pag) {
	$.ajax({
		data:{"pag":pag},
		url:"/proforma/proforma",
		type:"get",
		success:function(data){
			$("#tabla_contado").html(mostrar(data,pag));
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




$(document).ready(function(){
	contado(0);
});
