
function show_set(loaded_item)
{
   var url_str = loaded_item;
   var brchwin = window.open(url_str, 'branch', 'width=1000,height=600,status=no,resizable=yes,scrollbars=yes');
}

function autorizar (id) {
	val = document.getElementById('com_'+id);
	if(val.value==""){
		alert("por favor ingrese quien se va a LLEVAR EL PRODUCTO")
	}else{
		TAS_TIENDA(id,val.value,"V");
	}

}

function rechazar (id){
	val = document.getElementById('com_'+id);
	if(val.value==""){
		alert("explique porque fue RECHAZADO")
	}else{
		TAS_TIENDA(id,val.value,"F")
	}
}

function TAS_TIENDA (id,val,autorizada) {
    var message={
        action:"auth_traslado",
        id:id,
        val:val,
        autoriza:usuario,
        autorizada:autorizada
    };
    inter_tienda_socket.send(JSON.stringify(message));
    alert("solicitud enviada correctamente");
    return true;

}