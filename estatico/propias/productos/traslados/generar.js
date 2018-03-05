
var typingTimer; 
var doneTypingInterval = 500;


function count_consulta () {
	clearTimeout(typingTimer);
	typingTimer = setTimeout(doneTyping, doneTypingInterval);
}

function endcount(){
  clearTimeout(typingTimer);

}

function doneTyping () {
	var valor=document.getElementById('id_tienda').value;
	if (valor=="" || valor==null){
		alert("por favor primero seleccione una tienda");
	}else{
		page(0);
	}
}

function board(data,pag){
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>i</th><th>codigo</th><th>descripcion</th><th>marca</th><th>precio</th><th>cantidad</th><th>cargar</th></tr>";
	for(i=0;i<data.length;i++){
		var codigo =(data[i].producto__codigo.length>16)?data[i].producto__codigo.substr(0,12)+"...":data[i].producto__codigo;
		var descripcion =(data[i].producto__descripcion.length>16)?data[i].producto__descripcion.substr(0,12)+"...":data[i].producto__descripcion;
		var marca =(data[i].producto__marca.length>16)?data[i].producto__marca.substr(0,12)+"...":data[i].producto__marca;
		html+="<tr><td>"+String(i+1)+"</td><td>"+codigo+"</td><td>"+descripcion+"</td><td>"+marca+"</td>";
		html+="</td><td>"+data[i].tarjeta;
		html+="<td><select id='spin_"+data[i].producto__id+"'>";
		var spin =parseInt(data[i].cantidad);
		for (j=0;j<spin;j++){
			var val=j+1;
			html+="<option value='"+val+"'>"+val+"</option>";
		}
		html+="</select></td>";
		html+=" </td><td><button class='btn-success' onclick='load_data("+data[i].producto__id+")'>agregar</button></td></tr>";
	}
		


	var prev="", next="";
	if (pag!=0){
		p = pag-1;
		prev="<a onclick='page("+p+")' class='pull-right'><i class='fa fa-arrow-left pull-right' aria-hidden='true'></i></a>";
	}
	if(data.length==10)
	{
		p=pag+1;
		next="<a onclick='page("+p+")'><i class='fa fa-arrow-right' aria-hidden='true'></i></a>";
	}
	html = html+"<tr><td colspan='4'></td><td> "+prev+" </td><td> "+next+" </td><td></td> </tr></table></div>";
	return html;

}


function page(pag){
	$.ajax({
		data:{
			'codigo':document.getElementById('consultor').value,
			'tienda':valor=document.getElementById('id_tienda').value,
			'pagina':pag
		},
		url:'/inventario/consulta_pagina_tienda',
		type:'get',
		success:function(data){
			var d = board(data,pag)
			$('#inventario').html(d);
		}
	});
}






// segunda tabla

function display(pag){
	page_set(pag);
}


function load_data(valor) {
	$.ajax({ 
		data:{
			'tienda':document.getElementById('id_tienda').value,
			'producto':valor,
			'cantidad':document.getElementById('spin_'+valor).value,
			'csrfmiddlewaretoken':mitoken
		},
		url:'/bodega/traslados/cargar_a_lista/',
		type:'POST',
		success: function(data){
			$("#carga").html(load_tabla(data,0));
		}
	});
}


function pagina(numero){
	$.ajax({
		data:{
			"pag":numero,
			"doc":document.getElementById("info").value
		},
		url:'/productos/inventario/listar',
		type:'get',
		success:function(data){
			$("#carga").html(load_tabla(data,numero));

		}
	});
}

function total_ammount(){
	$.ajax({
		data:{
			"doc":document.getElementById("info").value
		},
		url:"/productos/inventario/total",
		type:"get",
		success:function(total){
			$("#valor_total").html("TOTAL:Q"+total);

		}

	})
}



function load_tabla (data,pag) {
	var ttl=0;
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th></th><th>codigo</th><th>descripcion</th><th>marca</th><th>cantidad</th><th>venta</th><th>total</th><th>quitar</th></tr>";
	for (i=0;i<data.length;i++){
		html+="<td>"+(i+1)+"</td>";
		html+="<td>"+data[i].producto__codigo+"</td>";
		html+="<td>"+data[i].producto__descripcion+"</td>";
		html+="<td>"+data[i].producto__marca+"</td>";
		html+="<td>"+data[i].cantidad+"</td>";
		html+="<td>"+data[i].venta+"</td>";
		var op = parseFloat(data[i].cantidad)*parseFloat(data[i].venta);
		html+="<td>"+op+"</td>";
		ttl=ttl+op;
		html+="<td><button class='btn btn-danger' onclick='dump_set("+data[i].producto__id+")'><i class='fa fa-trash-o' aria-hidden='true'></i></button></td></tr>";
	}
	html+="<td colspan=3></td>";
	prev="";
	next="";
	if (pag!=0){
		p = pag-1;
		prev="<a onclick='pagina("+p+")'><i class='fa fa-arrow-left' aria-hidden='true'></i></a>";
	}
	if(data.length==5)
	{
		p=pag+1;
		next="<a onclick='pagina("+p+")'><i class='fa fa-arrow-right' aria-hidden='true'></i></a>";
	}
	html+="<td>"+prev+"</td><td>"+next+"</td><td colspan=3> <h2><div id='valor_total'></div></h2></td></table></div>"
	total_ammount();
	return html;
}


function dump_set(valor){
	$.ajax({
		data:{
			'tienda':document.getElementById('id_tienda').value,
			'producto':valor,
			'csrfmiddlewaretoken':mitoken
		},
		url:'/bodega/traslados/quitar/',
		type:'POST',
		success:function(data){
			$("#carga").html(load_tabla(data,0));
		}
	});
}


function check (elemento,pag) {
	$.ajax({
		data:{
			"tienda":elemento.value,
			"pag":0

		},
		url:"/bodega/traslados/tienda",
		type:"get",
		success:function (data) {
			$("#carga").html(load_tabla(data,0));

		}
	});
}




$("#solicitar_tr").on("click", function(event) {

    var de = document.getElementById('id_tienda').value;
    var para=tienda;

    if (de==null || de=="" || de==0){
        alert("por favor seleccione una tienda");
    }else {
        var message={
            action:"traslado",
            de:de,
            para:para,
            usu:usuario,
        };
        inter_tienda_socket.send(JSON.stringify(message));
        alert("solicitud enviada correctamente");
        return true;
    }
    return false;
});