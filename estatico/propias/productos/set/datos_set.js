
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

	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>i</th><th>producto</th><th>descripcion</th><th>marca</th><th>cantidad</th><th>cargar</th></tr>";
	for(i=0;i<data.length;i++){
		var codigo =(data[i].codigo.length>16)?data[i].codigo.substr(0,12)+"...":data[i].codigo;
		var descripcion =(data[i].descripcion.length>16)?data[i].descripcion.substr(0,12)+"...":data[i].descripcion;
		var marca =(data[i].marca.length>16)?data[i].marca.substr(0,12)+"...":data[i].marca;
		html+="<tr><td>"+String(i+1)+"</td><td>"+codigo+"</td><td>"+descripcion+"</td><td>"+marca+"</td><td><input type='text' id='load_"+data[i].id+"' onkeypress='return event.charCode>=48 && event.charCode<=57'/> </td><td><button class='btn-success' onclick='load_set("+data[i].id+")'>agregar</button></td></tr>";
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
	html = html+"<tr><td colspan='4'></td><td> "+prev+" </td><td> "+next+" </td> </tr></table></div>";
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


function load_set(valor) {
	$.ajax({
		data:{
			'set':document.getElementById('store_Set').value,
			'producto':valor,
			'cantidad':document.getElementById('load_'+valor).value
		},
		url:'/productos/cargar_set',
		type:'get',
		success:function(data){
			page_set(0);
		}
	});
}





function dump_set(id,prod){
	$.ajax({
		data:{
			'set':id,
			'producto':prod,
		},
		url:'/productos/quitar_set',
		type:'get',
		success:function(data){
			page_set(0);
		}
	});
}


function tablizar_set(data,pag){
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th></th><th>producto</th><th>descripcion</th><th>marca</th><th>cantidad</th><th>quitar</th></tr>";
	for (i =0;i<data.length;i++){
		var codigo =(data[i].producto__codigo.length>16)?data[i].producto__codigo.substr(0,13)+"...":data[i].producto__codigo;
		var descripcion =(data[i].producto__descripcion.length>16)?data[i].producto__descripcion.substr(0,13)+"...":data[i].producto__descripcion;
		var marca =(data[i].producto__marca.length>16)?data[i].producto__marca.substr(0,13)+"...":data[i].producto__marca;
		html+="<tr><td>"+String(i+1)+"</td><td>"+codigo+"</td><td>"+descripcion+"</td><td>"+marca+"</td><td>"+data[i].cantidad+"</td><td><button class='btn-danger' onclick='dump_set("+'"'+data[i].id_set+'",'+data[i].producto+")'><i class='fa fa-trash-o' aria-hidden='true'></i></button></td></tr>";
	}
	var prev="", next="";
	if (pag!=0){
		p = pag-1;
		prev="<a onclick='page_set("+p+")'><i class='fa fa-arrow-left' aria-hidden='true'></i></a>";
	}
	if(data.length==10)
	{
		p=pag+1;
		next="<a onclick='page_set("+p+")'><i class='fa fa-arrow-right' aria-hidden='true'></i></a>";
	}
	html = html+"<tr><td colspan='4'></td><td> "+prev+" </td><td> "+next+" </td> </tr></table></div>";
	return html;

}

function page_set(pag){
	$.ajax({
		data:{
			'set':document.getElementById('store_Set').value,
			'pag':pag
		},
		url:'/productos/tabla_set',
		type:'get',
		success:function(data){
			var d=tablizar_set(data,pag);
			$('#lista').html(d);
		}
	});
}

