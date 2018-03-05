var modal = document.getElementById('myModal');

var btn = document.getElementById("id_nit");

var span = document.getElementsByClassName("close")[0];

document.getElementById("id_credito_a_registrar").setAttribute('onchange','lock_addr()');

span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onchange = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}




function byNit(){
	busca_por_nit(document.getElementById("id_nit").value);
}


function busca_por_nit(nit) {
	$("#tabla_pr").html("");
	$.ajax({
		data:{
			"nit":nit
		},
		url:"/clientes/nit",
		type:"get",
		success:function(data){
			try{
				document.getElementById('id_nit').value=data[0].info__nit;
				document.getElementById('id_nombre').value=data[0].info__nombre;
				document.getElementById('id_direccion').value=data[0].info__direccion;
				if (data[0].credito==false){
					$('#id_credito').attr("disabled",true);
					$('#id_credito').attr("checked",false);
				}else{
					$('#id_credito').removeAttr("disabled");
				}
			}catch(err){
				modal.style.display="block";
				document.getElementById("id_nit_a_registrar").value=document.getElementById("id_nit").value;
			}
		}
	});
}
var temporal="";
function lock_addr(){
	var d =document.getElementById("id_direccion_a_registrar");
	if (document.getElementById("id_credito_a_registrar").checked){
		temporal=d.value;
		d.value="CIUDAD";
		d.disabled=true;

	}else{
		d.value=temporal;
		d.disabled=false;

	}

}



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
		url:"/clientes/nombre",
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
		html+="<tr><td>"+data[i].info__nit+"</td><td>"+data[i].info__nombre+"</td><td><button onclick='busca_por_nit("+'"'+data[i].info__nit+'"'+")' class='btn-success'>seleccionar</button></td></tr>";
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





