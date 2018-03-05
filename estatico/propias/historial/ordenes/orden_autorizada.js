function show_set(loaded_item)
{

   var url_str = loaded_item;
   var brchwin = window.open(url_str, 'branch', 'width=1000,height=600,status=no,resizable=yes,scrollbars=yes');
   recargar(loaded_item);
}

function recargar(a_borrar){
	$.ajax({
		data:{
			"a_borrar":a_borrar,
			'csrfmiddlewaretoken':mitoken
		},
		type:"POST",
		url:"/orden_de_compra/quitar/",
		success:function(data){
			window.location.reload();

		}
	});

}