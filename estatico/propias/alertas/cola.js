
var ws_scheme_dispatch = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path_dispatch = ws_scheme_dispatch + '://' + window.location.host + '/cola';
console.log("Conectando a " + ws_path_dispatch)
cola_socket = new WebSocket(ws_path_dispatch);

cola_socket.onmessage = function(e) {
	var data =JSON.parse(e.data);
	if (data.tienda==tienda){
		var cantidad = data.cantidad;
		var producto = data.producto;
		var descripcion=data.descripcion;
		var marca=data.marca;
		var usu = data.solicita;
		var v_id=data.id;
		tabla(cantidad,producto,descripcion,marca,usu,v_id);
	}
}

if (cola_socket.readyState == WebSocket.OPEN) cola_socket.onopen();




function tabla (cantidad,producto,descripcion,marca,usu,v_id) {
	var tableRef = document.getElementById("mitabla");
	var newRow   = tableRef.insertRow(1);

	var cellId = newRow.insertCell(0)
	var cellUsu = newRow.insertCell(0)
	var celLMarca = newRow.insertCell(0)
	var cellDesc = newRow.insertCell(0)
	var cellProd = newRow.insertCell(0)
	var cellCant = newRow.insertCell(0)


	var l_cellId = document.createTextNode(v_id);
	var l_cellUsu = document.createTextNode(usu);
	var l_cellMarca = document.createTextNode(marca);
	var l_cellDesc = document.createTextNode(descripcion);
	var l_cellProd = document.createTextNode(producto);
	var l_cellCant = document.createTextNode(cantidad);

	cellUsu.appendChild(l_cellUsu);
	celLMarca.appendChild(l_cellMarca);
	cellDesc.appendChild(l_cellDesc);
	cellProd.appendChild(l_cellProd);
	cellCant.appendChild(l_cellCant);



	var btn = document.createElement('input');
	btn.type = "button";
	btn.className = "btn";
	btn.id = v_id;
	btn.value="Y";
	btn.classList.add('btn-success');
	btn.classList.add('btn-lg');
	btn.onclick = function() {quitar_de_lista(v_id)};
	cellId.appendChild(btn);


}

function quitar_de_lista (id) {
	$.ajax({
		data:{
			"id":id,
			"usu":document.getElementById("usuario_ddl").value,
			"csrfmiddlewaretoken":mitoken,
		},
		url:"/bodega/quitar/",
		type:"post",
		success:function(data){
			alert("SI")
		}

	});
	window.location.reload();
}

$(document).ready(function(){
	cola();
});

function cola () {
	$.ajax({
		url:"/bodega/lista",
		type:"get",
		success:function(data){
			for (i=0;i<data.length;i++){
				var cantidad=data[i].cantidad;
				var producto=data[i].producto__codigo__nombre;
				var descripcion =data[i].producto__descripcion__detalle;
				var marca = data[i].producto__marca__nombre;
				var usu = data[i].lista__ubicado__usuario__usuario__username;
				var v_id=data[i].id;
				tabla(cantidad,producto,descripcion,marca,usu,v_id);
			}
		}
	});
}
