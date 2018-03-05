function cambio_tienda () {
    var tienda = document.getElementById("id_tienda").value;
    $.ajax({
    	data:{
    		"tienda":tienda
    	},
    	url:"/conta/usuarios_por_tienda",
    	type:"get",
    	success:function(data){
    		$("#usuario").empty();
    		for(i=0;i<data.length;i++){
    			$("#usuario").append('<option value="'+data[i].id+'" selected="selected">'+data[i].usuario__username+' ('+data[i].puesto__nombre+')</option>')
    		}
    	}
    });
}

function asignar_doc () {
    $.ajax({
        data:{
            "tienda":document.getElementById('id_tienda').value,
            "usuario":document.getElementById('usuario').value,
            "serie":document.getElementById('id_serie').value,
            "documento":document.getElementById('id_documento').value,
            "csrfmiddlewaretoken":mitoken,
        },
        url:"/conta/documentos/",
        type:"POST",
        success:function (data) {
            if (data!="V"){
                alert(data);
            }else{
                alert("creado satisfactoriamente");
                window.location.reload();
            }
        }
    });
}