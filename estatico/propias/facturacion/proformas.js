
var typingTimer; 
var doneTypingInterval = 200;

var page_id="1";

function count_consulta () {
	clearTimeout(typingTimer);
	typingTimer = setTimeout(doneTyping, doneTypingInterval);
}

function endcount(){
  clearTimeout(typingTimer);

}

function doneTyping () {
	page(0);
}

function board(data,pag){
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>i</th><th>codigo</th><th>descripcion</th><th>marca</th><th>efectivo</th><th>tarjeta</th><th>cant.</th><th>cargar</th></tr>";
	for(i=0;i<data.length;i++){
		var codigo =(data[i].producto__codigo.length>16)?data[i].producto__codigo.substr(0,12)+"...":data[i].producto__codigo;
		var descripcion =(data[i].producto__descripcion.length>16)?data[i].producto__descripcion.substr(0,12)+"...":data[i].producto__descripcion;
		var marca =(data[i].producto__marca.length>16)?data[i].producto__marca.substr(0,12)+"...":data[i].producto__marca;
		html+="<tr><td>"+String(i+1)+"</td><td>"+codigo+"</td><td>"+descripcion+"</td><td>"+marca+"</td>";
		html+="<td>"+data[i].efectivo+"</td>";
		html+="</td><td><input type='text' id='venta_"+data[i].producto__id+"' onkeypress='return event.charCode>=48 && event.charCode<=57 || event.charCode==46' maxlength='12' size='12' placeholder='"+data[i].tarjeta+"'/>";
		var spin = parseInt(data[i].cantidad);
		html+="<td><select id='spin_"+data[i].producto__id+"'>";
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
	html = html+"<tr><td colspan='7'></td><td> "+prev+" </td><td> "+next+" </td><td></td> </tr></table></div>";
	return html;

}


function page(pag){
	$.ajax({
		data:{
			'codigo':document.getElementById('consultor').value,
			'pagina':pag
		},
		url:'/facturar/consulta_inv',
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
			'producto':valor,
			'cantidad':document.getElementById('spin_'+valor).value,
			'precio':document.getElementById('venta_'+valor).value,
			'csrfmiddlewaretoken':mitoken
		},
		url:'/proforma/cargar_a_lista/',
		type:'POST',
		success:function(data){
			if(data.includes("correctamente")){
				pagina(0);

			}else{
				alert(data);

			}
		}
	});




}


function pagina(numero){
	$.ajax({
		data:{
			"pag":numero,
			'indice':page_id
		},
		url:'/proforma/listar',
		type:'get',
		success:function(data){
			$("#carga").html(load_tabla(data,numero));

		}
	});
}

function total_ammount(){
	$.ajax({
		data:{
			"indice":page_id
		},
		url:"/proforma/total",
		type:"get",
		success:function(total){
			$("#valor_total").html("TOTAL:Q"+total);

		}

	})
}



function load_tabla (data,pag) {
	var ttl=0;
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th></th><th>codigo</th><th>descripcion</th><th>marca</th><th>cantidad</th><th>precio</th><th>total</th><th>quitar</th></tr>";
	for (i=0;i<data.length;i++){
		html+="<td>"+(i+1)+"</td>";
		html+="<td>"+data[i].producto__codigo+"</td>";
		html+="<td>"+data[i].producto__descripcion+"</td>";
		html+="<td>"+data[i].producto__marca+"</td>";
		html+="<td>"+data[i].cantidad+"</td>";
		html+="<td>"+data[i].unitario+"</td>";
		var op = parseFloat(data[i].cantidad)*parseFloat(data[i].unitario);
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

$(document).ready(function(){
	pagina(0);
});

function dump_set(prod){
	$.ajax({
		data:{
			'producto':prod,
			'indice':page_id,
			'csrfmiddlewaretoken':mitoken
		},
		url:'/proforma/quitar_prod/',
		type:'post',
		success:function(data){
			pagina(0);
		}
	});
}


function registrar_venta () {
	cliente = document.getElementById('cliente').value;
	telefono = document.getElementById('telefono').value;
	correo = document.getElementById('correo').value;
	$.ajax({
		data:{
			"cliente":cliente,
			"telefono":telefono,
			"correo":correo,
			"csrfmiddlewaretoken":mitoken,
		},
		url:"/proforma/imprimir/",
		type:"POST",
		success:function (data) {
			if (data.includes("vacia")){
				alert(data)
			}else{
				window.location.href="/proforma/"+data;
			}
		}
	});
	// window.location.reload();

}
