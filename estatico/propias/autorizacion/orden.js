


function cargar(pag){
	$.ajax({
		data:{
			"pag":pag
		},
		url:"/orden_de_compra/cargar_listado_credito",
		type:"get",
		success:function(data){
			$("#inventario").html(tabla_orden(data,pag));
		}

	});
}

function cargar2(pag){
	$.ajax({
		data:{
			"pag":pag
		},
		url:"/orden_de_compra/cargar_listado_contado",
		type:"get",
		success:function(data){
			$("#inventario2").html(tabla_orden(data,pag));
		}

	});
}

$(document).ready(function(){
	cargar(0);
	cargar2(0);
});

function tabla_orden(data,pag){
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>i</th><th>solicita</th><th>proveedor</th><th>fecha</th><th>total</th><th>comentario</th><th>rechazar</th><th>autorizar</th></tr>";
	for(i=0;i<data.length;i++){
		var solicita=data[i].solicita__usuario__username;
		var proveedor=data[i].proveedor__info__nombre;
		var fecha=data[i].fehca_registro;
		html+="<tr><td>"+String(i+1)+"</td><td>"+solicita+"</td><td>"+proveedor+"</td><td>"+fecha+"</td><td>"+data[i].lista__total+"</td>";
		html+="<td><input type='text' id='load_"+data[i].id+"'/> ";
		html+=" </td><td><button class='btn-danger' onclick='rechazar("+data[i].id+","+'"'+solicita+'"'+")'>---</button></td>";
		html+=" </td><td><button class='btn-success' onclick='autorizar("+data[i].id+")'>+++</button></td></tr>";
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
	html = html+"<tr><td colspan='4'></td><td> "+prev+" </td><td> "+next+" </td><td></td> </tr></table></div>";
	return html;

}

function rechazar(i,usu){
	if (confirm('seguro deseas rechazar esta solitud de "'+usu+'"?')) {
		var comentario=document.getElementById('load_'+i).value;
		if ((comentario==null )|| (comentario=="") ||(comentario.length<10)){
			alert("por favor, explique por que no se autorizo en la linea de comentario");
			return;
		}
		var message={
            action:"descartar_orden",
            info:i,
            comentario:comentario,
            usuario:usuario,
        };
        alert_socket.send(JSON.stringify(message));
        alert("la persona ha sido notificada correctamente");
		window.location.reload(true);
		
    
    }
}


function autorizar(i){
	alert("la persona ha sido notificada");
	var message={
        action:"autorizar_orden",
        info:i,
        usuario:usuario
    };
    alert_socket.send(JSON.stringify(message));
    window.location.reload(true);
}