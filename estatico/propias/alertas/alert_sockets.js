
var ws_scheme_alert = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path_alert = ws_scheme_alert + '://' + window.location.host + '/alertas';
console.log("Conectando a " + ws_path_alert)
alert_socket = new WebSocket(ws_path_alert);

alert_socket.onmessage = function(e) {
	var data =JSON.parse(e.data);
	var html='<div><i class="fa fa-comment fa-fw"></i> New Comment<span class="pull-right text-muted small">4 minutes ago</span></div>';
	if (data.tipo.includes("deposito")){
		deposito(data);
	}
	else if(data.tipo=="alerta"){
		puesto(data);	
	}else if(data.tipo=="notificacion"){
		if(data.solicita==usuario){
			$("#proceso").css({'background-color':'#F5F5F5', 'color': '#7FFF00'});
			$("#proceso").addClass('fa-3x');
			var proceso="";
			if(data.principal.includes("rechazada")){
				var up="<li><a href='#'><div><i class='fa fa-remove fa-fw'></i>";var mid="<span class='pull-right text-muted small'>";
				var end="</span></div></a></li>";
				proceso=up+data.principal+mid+data.instruccion+end+"<li class='divider'></li>";	
			}else{
				var up="<li><a href='#'><div><i class='fa fa-check-circle-o fa-fw'></i>";var mid="<span class='pull-right text-muted small'>";
				var end="</span></div></a></li>";
				proceso=up+data.principal+mid+data.instruccion+end+"<li class='divider'></li>";
			}
			$("#ddl_proceso").append(proceso);
		}
	}else if(data.tipo=="listar_productos"){
		alert(":;)");
	}else if(data.tipo=="fracaso"){
		if (usuario==data.solicita){
			alert(data.principal);
		}
	}

}
if (alert_socket.readyState == WebSocket.OPEN) alert_socket.onopen();

function puesto(datos){
	$.ajax({
		data:{
			"puesto":datos.puesto
		},
		url:"/puesto",
		type:"get",
		success:function(data){
		$("#alertas").css({'background-color':'#F5F5F5', 'color': 'red'});
		$("#alertas").addClass('fa-3x');		
		var up="<li><a href='"+datos.ruta+"'><div><i class='fa fa-upload fa-fw'></i>";var mid="<span class='pull-right text-muted small'>";
		var end="</span></div></a></li>";
		var alerta=up+datos.principal+mid+datos.solicita+" solicita "+datos.instruccion+end+"<li class='divider'></li>";
		$("#ddl_alertas").append(alerta);
		}
	});
}

function deposito (datos) {
	if (usuario==datos.solicita){
		$("#alertas").css({'background-color':'#F5F5F5', 'color': '#66b3ff'});
		$("#alertas").addClass('fa-3x');
		var icono=""
		if (datos.tipo=="depositoF"){
			icono="fa-thumbs-o-up";

		}else if(datos.tipo=="depositoR"){
			icono="fa-thumbs-o-down"

		}else{
			icono="fa-ticket"

		}		
		var up="<li><a href='"+datos.ruta+"'><div><i class='fa "+icono+" fa-fw'></i>";
		var mid="<span class='pull-right text-muted small'>";
		var end="</span></div></a></li>";
		
		var alerta=up+datos.principal+mid+datos.instruccion+end+"<li class='divider'></li>";
		$("#ddl_alertas").append(alerta);
		

	}
}