function registrar_compra(){
	var doc=document.getElementById("documento").value;
	var nit=document.getElementById("id_nit").value;
	var info=document.getElementById("info").value;
	var credito=document.getElementById("id_credito").checked;
	var fecha = document.getElementById("fecha").value;
	if (fecha==""){
		alert("por favor ingrese la fecha de la compra");
	}else if (nit==""){
		alert("por favor ingrese el nit del proveedor");

	}else if(doc==""){
		alert("por favor ingrese un numero de documento");
	}else{
		cargar_documento(doc,nit,info,credito,fecha);
	}
	
}

function cargar_documento (doc,nit,info,credito,fecha) {
	$.ajax({
		data:{
			"doc":doc,
			"nit":nit,
			"info":info,
			"credito":credito,
			"fecha":fecha,
			"csrfmiddlewaretoken":mitoken,
		},
		url:"/productos/compras/registrar_compra/",
		type:"post",
		success:function (data) {
			if(data=="V"){
				window.location.reload(true); 
			}else{
				alert(data);
			}
		}
	});
}

