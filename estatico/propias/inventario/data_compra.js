
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
	page(0);
}

function board(data,pag){
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>i</th><th>codigo</th><th>descripcion</th><th>marca</th><th>cantidad</th><th>precio</th><th>cargar</th></tr>";
	for(i=0;i<data.length;i++){
		var codigo =(data[i].codigo.length>16)?data[i].codigo.substr(0,12)+"...":data[i].codigo;
		var descripcion =(data[i].descripcion.length>16)?data[i].descripcion.substr(0,12)+"...":data[i].descripcion;
		var marca =(data[i].marca.length>16)?data[i].marca.substr(0,12)+"...":data[i].marca;
		html+="<tr><td>"+String(i+1)+"</td><td>"+codigo+"</td><td>"+descripcion+"</td><td>"+marca+"</td>";
		html+="<td><input type='text' id='load_"+data[i].id+"' onkeypress='return event.charCode>=48 && event.charCode<=57'/> ";
		html+="</td><td><input type='text' id='val_"+data[i].id+"' onkeypress='return event.charCode>=48 && event.charCode<=57 || event.charCode==46'/>";
		html+=" </td><td><button class='btn-success' onclick='load_data("+data[i].id+")'>agregar</button></td></tr>";
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
			'pagina':pag
		},
		url:'/productos/consulta_pagina',
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
			'cantidad':document.getElementById('load_'+valor).value,
			'precio':document.getElementById('val_'+valor).value,
			'csrfmiddlewaretoken':mitoken
		},
		url:'/orden_de_compra/cargar_a_lista_compra/',
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
			"pag":numero
		},
		url:'/orden_de_compra/listar_compra',
		type:'get',
		success:function(data){
			$("#carga").html(load_tabla(data,numero));

		}
	});
}

function total_ammount(){
	$.ajax({
		url:"/orden_de_compra/total_compra",
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
			'csrfmiddlewaretoken':mitoken
		},
		url:'/orden_de_compra/quitar_prod_compra/',
		type:'post',
		success:function(data){
			pagina(0);
		}
	});
}

function registrar_compra(){
	documento = document.getElementById("documento").value;
	fecha = document.getElementById("fecha").value;
	nit=document.getElementById("id_nit").value;
	credito = document.getElementById("id_credito").checked;
	if (documento==null || documento==""){
		alert("favor ingrese el numero de documento");
	}else if (fecha==""){
		alert("favor ingrese la fecha del documento");
	}else if(nit =="" || nit==null){
		alert("favor ingrese un numero de nit valido");
	}
	else{
		cargar_compra(documento,fecha,nit,credito);
	}
}

function cargar_compra(d,f,n,c){
	$.ajax({
		data:{
			"documento":d,
			"fecha":f,
			"nit":n,
			"credito":c,
			"csrfmiddlewaretoken":mitoken,
		},
		url:"/productos/compras/registrar_compra/",
		type:"POST",
		success:function (data) {
			alert(data);
		}

	});

}
