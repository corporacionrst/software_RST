var typingTimer; 
var doneTypingInterval = 500;


function count_consulta () {
	clearTimeout(typingTimer);
	typingTimer = setTimeout(doneTyping, doneTypingInterval);
}

function endcount(){
  clearTimeout(typingTimer);

}

function doneTyping () {
	page(0);
}




function board(data,pag){

	var html="<div class='table-responsive'><table class='table table-striped table-bordered table-hover'><tr><th>producto</th><th>descripcion</th><th>marca</th><th>cantidad</th><th>mayorista</th><th>efectivo</th><th>tarjeta</th></tr>";
	for(i=0;i<data.length;i++){
		var codigo =(data[i].producto__codigo.length>16)?data[i].producto__codigo.substr(0,12)+"...":data[i].producto__codigo;
		var descripcion =(data[i].producto__descripcion.length>16)?data[i].producto__descripcion.substr(0,12)+"...":data[i].producto__descripcion;
		var marca =(data[i].producto__marca.length>16)?data[i].producto__marca.substr(0,12)+"...":data[i].producto__marca;
		html+="<tr><td><a href='javascript: show_set("+data[i].producto__id+");'>"+codigo+"</a></td><td>"+descripcion+"</td><td>"+marca+"</td><td>"+data[i].cantidad+"</td><td>"+data[i].mayorista+"</td><td>"+data[i].efectivo+"</td><td>"+data[i].tarjeta+"</td></tr>";
	}
	var prev="", next="";
	if (pag!=0){
		p = pag-1;
		prev="<a onclick='page("+p+")' class='pull-right'><i class='fa fa-arrow-left pull-right' aria-hidden='true'></i>;)</a>";
	}
	if(data.length==10)
	{
		p=pag+1;
		next="<a onclick='page("+p+")'><i class='fa fa-arrow-right' aria-hidden='true'></i></a>";
	}
	html = html+"<tr><td colspan='5'></td><td> "+prev+" </td><td> "+next+" </td> </tr></table></div>";
	return html;

}


function page(pag){
	$.ajax({
		data:{
			'codigo':document.getElementById('consultor').value,
			'pagina':pag
		},
		url:'/inventario/inventario_local',
		type:'get',
		success:function(data){
			var d = board(data,pag)
			$('#inventario').html(d);
		}
	});
}


function show_set (id) {	
   var brchwin = window.open(id, 'branch', 'width=500,height=800,status=no,resizable=yes,scrollbars=yes');
}
