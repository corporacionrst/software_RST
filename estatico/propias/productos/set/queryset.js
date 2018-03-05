
var typingTimer_set; 
var doneTypingIntervalsearch = 500;


function look_consulta () {
	clearTimeout(typingTimer_set);
	typingTimer_set = setTimeout(doneTypingsearch, doneTypingIntervalsearch);
}

function endcountlook(){
  clearTimeout(typingTimer_set);

}

function doneTypingsearch () {
	otra_pagina(0);
}

function board_set(data,pag){
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th></th><th>codigo</th><th>descripcion</th><th>marca</th><th>cargar</th></tr>";
	for(i=0;i<data.length;i++){
		var codigo =(data[i].codigo.length>16)?data[i].codigo.substr(0,12)+"...":data[i].codigo;
		var descripcion =(data[i].descripcion.length>16)?data[i].descripcion.substr(0,12)+"...":data[i].descripcion;
		var marca =(data[i].marca.length>16)?data[i].marca.substr(0,12)+"...":data[i].marca;
		html+="<tr><td>"+String(i+1)+"</td><td>"+codigo+"</td><td>"+descripcion+"</td><td>"+marca+"</td><td><button class='btn-success' onclick='selection("+'"'+data[i].codigo+'","'+data[i].descripcion+'","'+data[i].marca+'",'+data[i].id+")'>seleccionar</button></td></tr>";
	}
	var prev="", next="";
	if (pag!=0){
		p = pag-1;
		prev="<a onclick='otra_pagina("+p+")' class='pull-right'><i class='fa fa-arrow-left pull-right' aria-hidden='true'></i></a>";
	}
	if(data.length==10)
	{
		p=pag+1;
		next="<a onclick='otra_pagina("+p+")'><i class='fa fa-arrow-right' aria-hidden='true'></i></a>";
	}
	html = html+"<tr><td colspan='3'></td><td> "+prev+" </td><td> "+next+" </td> </tr></table></div>";
	return html;

}


function otra_pagina (val) {
	$.ajax({
		data:{
			'codigo':document.getElementById('consultor_check').value,
			'pagina':val
		},
		url:'/productos/consulta_pagina',
		type:'get',
		success:function(data){
			var d=board_set(data,val);
			$('#productos_a_listar').html(d);
		}
	});
}


function selection (codigo,descripcion,marca,arg) {
	$.ajax({
		data:{
			'producto':arg
		},
		url:'/productos/obtener',
		type:'get',
		success:function (data) {
			document.getElementById("id_codigo").value=codigo;
			document.getElementById("id_descripcion").value=descripcion;
			document.getElementById("id_marca").value=marca;
			document.getElementById("id_codigo").disabled=true;
			document.getElementById("id_descripcion").disabled=true;
			document.getElementById("id_marca").disabled=true;
			document.getElementById("store_Set").value=data;
			var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th></th><th>codigo</th><th>descripcion</th><th>marca</th><th>cargar</th></tr>";
			html = html+"<tr><td colspan='3'></td><td> </td><td> </td> </tr></table></div>";
			$('#productos_a_listar').html(html);
			document.getElementById("prod_id_store").value=arg;

			document.getElementById('rowset').hidden=false;
			page_set(0);

		}
	});
}

function store () {
	$.ajax({
		data:{
			'producto':document.getElementById("prod_id_store").value,
			'set':document.getElementById("store_Set").value
		},
		url:'/productos/asignar_set',
		type:'get',
		success:function (data) {
			alert("exitosamente combinado");
			window.location = "/productos/set/";
		}
	});

}


