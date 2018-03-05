
var byDate_dispath = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path_date = byDate_dispath + '://' + window.location.host + '/salarios';
console.log("Conectando a " + ws_path_date)
show_date = new WebSocket(ws_path_date);


function buscar_por_fecha () {
	var desde=document.getElementById('de').value;
	var hasta=document.getElementById('a').value;
	var message={
		"action":"fecha_de_salario",
		"desde":desde,
		"hasta":hasta,
		"usuario":usu,
	}
	$("#id_tabla tr").remove(); 
	var tabla=document.getElementById('id_tabla');
	var fila=tabla.insertRow();

	show_date.send(JSON.stringify(message));
	llamarGrafica(usu)

}

function llamarGrafica(usu){
	var endpoint = '/admin/usuarios/seguimiento';
    var Default_data=[];
    var labels=[];
    $.ajax({
        method:"GET",
        data:{"usuario":usu},
        url:endpoint,
        success:function (data) {
            var ctx = document.getElementById("myChart").getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'ultimo año(anterior-actual)',
                        data: data.default_val,
                        backgroundColor: data.bgcolor,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });




        },
        error:function (data) {
            console.log(error_data)
        }
    })


}


show_date.onmessage = function(e) {
	var data =JSON.parse(e.data);
	var facturas_del_mes='<button class="btn btn-lg btn-primary"><i class="fa fa-eye fa-lg" aria-hidden="true"></i></button>'
	facturas_del_mes=(data.facturas_del_mes!="")?data.facturas_del_mes:facturas_del_mes;
	
	if (data.tipo=="tabla"){
		$("#id_tabla tr:last").after('<tr><td>'+data.fecha_de_pago+'</td><td>'+data.salario+'</td><td>'+data.comision+'</td><td>'+data.total+'</td><td>'+facturas_del_mes+'</td></tr>');
	}else{
		$("#informacion").html=data.informacion;
	}
}



if (show_date.readyState == WebSocket.OPEN) show_date.onopen();


function historial_permisos () {
	$.ajax({
		data:{"usuario":usu},
		url:"/permisos",
		type:"get",
		success:function (data) {

		}


	});
}
