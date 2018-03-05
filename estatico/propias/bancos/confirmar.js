


function cargar(pag){
	$.ajax({
		data:{
			"pag":pag
		},
		url:"/caja/depositos/cola",
		type:"get",
		success:function(data){
			$("#inventario").html(tabla_orden(data,pag));
		}

	});
}


$(document).ready(function(){
	cargar(0);
});

function tabla_orden(data,pag){

	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>i</th><th>envia</th><th>de cuenta</th><th>documento</th><th>a mi cuenta</th><th>monto</th><th>no recibido</th><th>confirmado</th></tr>";
	for(i=0;i<data.length;i++){
		var solicita=data[i].cuenta_debitada__administra__usuario__username;
		var proveedor=data[i].cuenta_debitada__banco+" NO:"+data[i].cuenta_debitada__numero_de_cuenta;
		var fecha=data[i].cuenta_acreditada__numero_de_cuenta;
		html+="<tr><td>"+String(i+1)+"</td><td>"+solicita+"</td><td>"+proveedor+"</td><td>"+data[i].documento+"</td><td>NO:"+fecha+"</td><td>"+data[i].monto+"</td>";
		html+=" </td><td><button class='btn-danger btn-lg' onclick='rechazar("+data[i].id+")'>X</button></td>";
		html+=" </td><td><button class='btn-success btn-lg' onclick='autorizar("+data[i].id+")'>aceptar</button></td></tr>";
	}
	var prev="", next="";
	if (pag!=0){
		p = pag-1;
		prev="<a onclick='cargar("+p+")' class='pull-right'><i class='fa fa-arrow-left pull-right' aria-hidden='true'></i></a>";
	}
	if(data.length==10)
	{
		p=pag+1;
		next="<a onclick='cargar("+p+")'><i class='fa fa-arrow-right' aria-hidden='true'></i></a>";
	}
	html = html+"<tr><td colspan='5'></td><td> "+prev+" </td><td> "+next+" </td><td></td> </tr></table></div>";
	return html;

}

function rechazar(i){
	if (confirm('¿no recibiste este deposito?')) {
		var message={
            action:"descartar_deposito",
            info:i
        };
        alert_socket.send(JSON.stringify(message));
        alert("la persona ha sido notificada");
		window.location.reload(true);
		
    
    }
}


function autorizar(i){
	alert("la persona ha sido notificada");
	var message={
        action:"autorizar_deposito",
        info:i
    };
    alert_socket.send(JSON.stringify(message));
    alert("se ha acreditado a tu cuenta");
    window.location.reload(true);
}