
function registrar_venta (id) {
	var nit =document.getElementById('id_nit').value;
	var credito =document.getElementById('id_credito').checked;
	if(nit=="" || nit==null){
		alert("el nit no puede permanecer vacio")
	}else{
		$.ajax({
			data:{
				"nit":nit,
				"credito":credito,
				"proforma":id,
				"csrfmiddlewaretoken":mitoken,
			},
			url:"/proforma/ver/"+id+"/",
			type:"post",
			success:function (data) {
				alert(data);
				window.location.href="/";
			}
		})
	}
	
}