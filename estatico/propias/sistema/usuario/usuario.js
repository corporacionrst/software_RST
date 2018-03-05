function eliminar (id,usuario) {
	var vf =confirm("¿esta seguro que desea eliminar a "+usuario+"?");
	if (vf){
		$.ajax({
			data:{
				"usuario":id
			},
			url:"/admin/usuarios/eliminar",
			type:'get',
			success:function (data) {
				alert(data.usu);
			}
		});
	}
	window.location.reload();
}

