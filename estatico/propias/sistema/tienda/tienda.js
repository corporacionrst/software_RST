function registrar () {
	$.ajax({
		data:{
			"nombre":document.getElementById('id_nombre').value,
			"addr":document.getElementById('id_direccion').value,
			"tel":document.getElementById('id_telefono').value,
			"admin":document.getElementById('id_admin').value,
		},
		url:"agregar",
		type:"get",
		success:function (data) {
			alert(data);
		}
	});
}

function refactorizar(){
	$.ajax({
		data:{
			"tienda":document.getElementById('id_tienda').value
		},
		url:"refactorizar",
		type:"get",
		success:function (data) {
			alert(data);
		}
	});
}