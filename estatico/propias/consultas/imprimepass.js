

function contrasena_lista(nit,actual){
	$.ajax({
		data:{
			"nit":nit,
			"actual":actual

		},
		type:"get",
		url:"/caja/contrasenas/showpasswd",
		success:function (table) {
			tabla(table);
		}
	});
}

function tabla (data) {
	$("#lista_contras").html(tabla_AC(data));


}

function tabla_AC (data) {
	var totalPag=0;
	var html="<tr><th>serie</th><th>documento</th><th>emision</th><th>total</th></tr>";
	var total=0;
	for (var i = 0; i<10; i++) {
		if (i<data.length){
			total=parseFloat(data[i].lista__total);
			totalPag+=parseFloat(total);
			html+="<tr><td>"+data[i].documento__serie+"</td><td>"+data[i].documento__documento+"</td><td>"+data[i].fecha_registro+"</td><td>"+data[i].lista__total+"</td></tr>";
		}
		else{
			html+="<tr><td colspan='4'>.</td></tr>"
		}
	};

	html+="<tr><td colspan=3><div id='teletras'></div></td><td>"+totalPag+"</td></tr>"
	$("#total_ammount").html("TOTAL:"+currency+totalPag);
	total_a_texto(totalPag);
	return html;
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

		
