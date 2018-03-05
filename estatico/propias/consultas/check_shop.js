function check_shop (val) {
	if (val==1){
		valor=document.getElementById('nit').value;
	}else{
		valor=document.getElementById('documento').value;
	}
	$("#detalle").html("");
	aj(valor,val,0);
}

function aj(valor,val,pag){

	$.ajax({
		data:{
			"busca":valor,
			"index":val,
			"pag":pag,
		},
		url:"/productos/compras/documento",
		type:"get",
		success:function(data){
			$("#productos").html(tabla(data,pag,val,valor));
		}
	});
}

function tabla (data,pag,val,valor) {
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>i</th><th>documento</th><th>tipo</th><th>proveedor</th><th>total</th><th>cargado por</th></tr>";
	for(i=0;i<data.length;i++){
		var documento =data[i].documento;
		var proveedor =data[i].cliente_proveedor__nit;
		var total =data[i].lista__total;
		var url = data[i].lista__id;
		var tipo = (data[i].tipo=="CC")?"COMPRA CONTADO":"COMPRA CREDITO";
		html+="<tr><td>"+(i+1)+"</td><td><button class='btn-primary btn-lg' onclick='ver_documento("+'"'+url+'","'+documento+'","'+proveedor+'","'+total+'",0'+")' >"+documento+"</button></td><td>"+tipo+"</td><td>"+proveedor+"</td><td>"+total+" </td><td>"+data[i].ingresa__usuario__username+"</td></tr>";
	}
	var prev="", next="";
	if (pag!=0){
		p = pag-1;
		prev="<a onclick='aj("+'"'+valor+'"'+","+'"'+val+'"'+","+p+")' class='pull-right'><i class='fa fa-arrow-left pull-right' aria-hidden='true'></i></a>";
	}
	if(data.length==10)
	{
		p=pag+1;
		next="<a onclick='aj("+'"'+valor+'"'+","+'"'+val+'"'+","+p+")'><i class='fa fa-arrow-right' aria-hidden='true'></i></a>";
	}
	html = html+"<tr><td colspan='4'></td><td> "+prev+" </td><td> "+next+" </td> </tr></table></div>";
	return html;
}


function ver_documento (val,doc,prov,total,pag) {
	var pg="<table class='table table-striped table-bordered table-hover'><tr><th>documento</th><th>proveedor</th><th>total</th></tr>";
	pg+="<tr><td>"+doc+"</td><td>"+prov+"</td><td>"+total+"</td></tr></table>";
	$("#detalle").html(pg);
	preview(val,pag);

}

function preview(val,pag){
	$.ajax({
		data:{
			"documento":val,
			"pag":pag
		},
		url:"/productos/compras/detallar_compra",
		type:"get",
		success:function(data){
			$("#productos").html(vista_previa(data,pag,val))
		}
	});
}


function vista_previa (data,pag,val) {
	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>i</th><th>codigo</th><th>descripcion</th><th>marca</th><th>cantidad</th><th>unitario</th><th>total</th></tr>";
	var st=0
	for(i=0;i<data.length;i++){
		var codigo =data[i].producto__codigo;
		var descripcion =data[i].producto__descripcion;
		var marca =data[i].producto__marca;
		var cantidad = data[i].cantidad;
		var unitario = data[i].unitario;
		var total = parseFloat(data[i].cantidad)*parseFloat(data[i].unitario);
		st=st+total;
		html+="<tr><td>"+(i+1)+"</td><td>"+codigo+"</td><td>"+descripcion+"</td><td>"+marca+"</td><td>"+cantidad+" </td><td>"+unitario+"</td><td>"+total+"</td></tr>";
	}
	var prev="", next="";
	if (pag!=0){
		p = pag-1;
		prev="<a onclick='preview("+val+","+p+")' class='pull-right'><i class='fa fa-arrow-left pull-right' aria-hidden='true'></i></a>";
	}
	if(data.length==10)
	{
		p=pag+1;
		next="<a onclick='preview("+val+","+p+")'><i class='fa fa-arrow-right' aria-hidden='true'></i></a>";
	}
	html = html+"<tr><td colspan='4'></td><td> "+prev+" </td><td> "+next+" </td> <td>total:Q"+st+"</td></tr></table></div>";
	return html;
}


