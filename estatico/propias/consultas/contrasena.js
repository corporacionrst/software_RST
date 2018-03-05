var typingTimer_provider; 
var doneTypingInterval_nombre = 800;


function count_nombre () {
	clearTimeout(typingTimer_provider);
	typingTimer_provider = setTimeout(doneTyping_nombre, doneTypingInterval_nombre);
}

function endnombre(){
  clearTimeout(typingTimer_provider);

}

function doneTyping_nombre () {
	porNombre(0);
}

function porNombre(pag){
	$.ajax({
		data:{
			'nombre':document.getElementById("id_nombre").value,
			'pag':pag
		},
		url:"/proveedores/nombre",
		type:"get",
		success:function(data){
			$("#tabla_pr").html(tabla(data,pag));

		}
	});
}

function tabla(data,pag){
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>nit</th><th>nombre</th><th>seleccionar</th></tr>";
	var longitud = data.length;
	for (var i = 0; i<longitud; i++) {
		html+="<tr><td>"+data[i].info__nit+"</td><td>"+data[i].info__nombre+"</td><td><button onclick='busca_por_nit("+'"'+data[i].info__nit+'"'+",0)' class='btn-success'>seleccionar</button></td></tr>";
	};
	html+="<tr><td></td>";
	if(pag!=0){
		var p=parseInt(pag)-1; 
		html+="<td><button onclick='porNombre("+p+")' class='btn-warning pull-right'><i class='fa fa-arrow-left' aria-hidden='true'></i></button></td>";
	}else{
		html+="<td></td>";
	}
	if (longitud==2){
		var p=parseInt(pag)+1; 
		
		html+="<td><button onclick='porNombre("+p+")' class='btn-warning'><i class='fa fa-arrow-right' aria-hidden='true'></i></button></td></tr>";

	}else{
		html+="<td></td></tr>";
	}

	return html;
}
function busca_por_nit(data,pag){
	$.ajax({
		data:{
			"nit":data
		},
		url:"por_nit",
		type:"get",
		success:function(exito){
			document.getElementById('no_con').value=data;
			$("#tr").html(listar_contras(exito,pag));
			contrasena_lista();
			showprinter();
		}
	});
}

function contrasena_lista(){
	$.ajax({
		data:{
			"nit":document.getElementById('no_con').value
		},
		type:"get",
		url:"lista_de_contrasena",
		success:function (data) {
			$("#lista_contras").html(tabla_AC(data));
		}
	});

}


function listar_contras (data,pag) {
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>orden</th><th>nit</th><th>nombre</th><th>total</th><th>serie</th><th>documento</th><th>agregar</th></tr>";
	var longitud = data.length;
	for (var i = 0; i<longitud; i++) {
		html+="<tr><td>"+data[i].id+"</td><td>"+data[i].proveedor__info__nit+"</td><td>"+data[i].proveedor__info__nombre+"</td><td>"+data[i].lista__total+"</td><td><input type='text' id='serie_"+data[i].id+"' maxlength=5 size=5/></td><td><input type='text' id='tb_"+data[i].id+"'/></td><td><button onclick='agregar_a_contrasena("+'"'+data[i].id+'"'+")' class='btn-success'>agregar a contraseña</button></td></tr>";
	};
	html+="<tr><td></td>";
	if(pag!=0){
		var p=parseInt(pag)-1; 
		html+="<td><button onclick='porNombre("+p+")' class='btn-warning pull-right'><i class='fa fa-arrow-left' aria-hidden='true'></i></button></td>";
	}else{
		html+="<td></td>";
	}
	if (longitud==10){
		var p=parseInt(pag)+1; 
		
		html+="<td><button onclick='porNombre("+p+")' class='btn-warning'><i class='fa fa-arrow-right' aria-hidden='true'></i></button></td></tr>";

	}else{
		html+="<td></td></tr>";
	}

	return html;
}

function agregar_a_contrasena(id){
	var elemento =document.getElementById("tb_"+id).value
	var serie =document.getElementById("serie_"+id).value
	evaluaCon(id,serie,elemento);
	showprinter();
}
function evaluaCon(id,serie,elemento){
	$.ajax({
		data:{
			"documento" : id,
			"numero": elemento,
			"serie":serie,
			"csrfmiddlewaretoken":mitoken
		},
		url:"cargar/",
		type:"POST",
		success:function(data){
			if (data=="+"){
				contrasena_lista();
			}else{
				alert(data);
			}
		}
	});
}



function tabla_AC (data) {
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>orden</th><th>serie</th><th>documento</th><th>total</th><th>quitar</th></tr>";
	for (var i = 0; i<data.length; i++) {
		html+="<tr><td>"+data[i].id+"</td><td>"+data[i].documento__serie+"</td><td>"+data[i].documento__documento+"</td><td>"+data[i].lista__total+"</td><td><button onclick='quitar_contrasena("+'"'+data[i].id+'"'+")' class='btn-danger'>quitar de contraseña</button></td></tr>";
	};
	return html;
}
function imprimir_contrasena (url) {
	if (url=="-1"){
		alert("la contraseña parece estar vacia");
	}else
	{
		update_con();
		var brchwin = window.open(url, 'branch', 'width=1000,height=600,status=no,resizable=yes,scrollbars=yes');
		window.location.reload();

	}
		
}

function showprinter () {
	$.ajax({
		data:{
			"nit":document.getElementById('no_con').value,
		},
		type:"get",
		url:"imprimir",
		success:function (data) {
			$("#my_showprinter").html('<a href="javascript: imprimir_contrasena('+data+');"><i class="fa fa-eye fa-3x" aria-hidden="true" >vista previa</i> </a>');
		}

	})
}

function update_con () {
	$.ajax({
		data:{
			"nit":document.getElementById('no_con').value,
			"csrfmiddlewaretoken":mitoken
		},
		type:"post",
		url:"imprimir/",
	});
}


function quitar_contrasena (id) {
	remove_pass(id);
	showprinter();
}


function remove_pass (id) {
	$.ajax({
		data:{
			"documento" : id,
			"csrfmiddlewaretoken":mitoken
		},
		url:"quitar/",
		type:"POST",
		success:function(data){
			if (data=="+"){
				contrasena_lista();
			}else{
				alert(data);
			}
		}
	});
}
		
