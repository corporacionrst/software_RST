function cargarTabla(pag){
	$.ajax({
		data:{
			"documento":lista_id,
			"pag":pag
		},
		url:"/historial/listar_producto",
		type:"get",
		success:function(data){
			tabla(data);
		}

	});
}
function tabla (data) {
	var tableRef = document.getElementById("mitabla");
	var totalPag=0;
	for(i=0;i<10;i++){
		var newRow   = tableRef.insertRow(i+7);
		if(i<data.length){
			var codigo = data[i].producto__codigo;
			var descr = data[i].producto__descripcion;
			var pmd=data[i].producto__marca__definicion;
			var pmn=data[i].producto__marca__nombre;
			try{
				pmd.includes("undefined");					
				var marca =pmd;
			}catch(err){
				var marca=pmn;
			}
			
			var cantidad = data[i].cantidad;
			var unitario = data[i].unitario;
			
			var u_predictivo=unitario.split('.');
			unitario=(u_predictivo.length==1)?unitario+".00":(u_predictivo[1].length<2)?unitario:u_predictivo[0]+"."+u_predictivo[1][0]+u_predictivo[1][1];
			
			var total = parseFloat(cantidad)*parseFloat(unitario);
			totalPag+=total;
			var t_predictivo = toString(total).split('.');
			total=(t_predictivo.length==1)?total+".00":total;
			

			var cellTotal  = newRow.insertCell(0);
			var cellUnit  = newRow.insertCell(0);
			var cellDescr  = newRow.insertCell(0);
			cellDescr.colSpan=3;
			var cellMarca  = newRow.insertCell(0);
			var cellCant  = newRow.insertCell(0);
			// generar columnas
			var l_cantidad = document.createTextNode(cantidad);
			var l_marca = document.createTextNode(marca);
			var l_codigo = document.createTextNode(codigo);
			var l_decripcion = document.createTextNode(descr+" "+codigo);
			var l_unitario = document.createTextNode(currency+unitario);
			var l_total = document.createTextNode(currency+total);
			// 

		// concatenar
			cellCant.appendChild(l_cantidad);
			cellMarca.appendChild(l_marca);
			cellDescr.appendChild(l_decripcion);
			cellUnit.appendChild(l_unitario);
			cellTotal.appendChild(l_total);
		}
		else{
			var newCell  = newRow.insertCell(0);
			var nl_codigo = document.createTextNode("-");
			newCell.colSpan=7;
			newCell.appendChild(nl_codigo);
		}
	}
	$("#total_ammount").html("TOTAL:"+currency+totalPag);
	total_a_texto(totalPag);


}
function total_a_texto(total){
	$.ajax({
		data:{
			"total":total,
			"moneda":currency,
		},
		url:'/tienda/total_en_lentras',
		type:"get",
		success:function(numero_a_letras){
			$("#teletras").html("total en letras: "+numero_a_letras);
		}

	});

}


function change_page (pag) {
	cargarTabla(pag);
}