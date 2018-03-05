

function alertas(){
$.ajax({
        url:"/alertas/bell",
        type:"get",
        success:function(data){
            if (data.length>0){
                for(var i=0;i<data.length;i++){
                    $("#alertas").css({'background-color':'#F5F5F5', 'color': 'red'});
                    $("#alertas").addClass('fa-3x');
                    var up="<li><a href='"+data[i].ruta+"'><div><i class='fa fa-upload fa-fw'></i>";
                    var mid="<span class='pull-right text-muted small'>";
                    var end="</span></div></a></li>";
                    var alerta=up+data[i].mensaje+mid+data[i].requiere__usuario__username+" solicita "+data[i].sub_mensaje+end+"<li class='divider'></li>";
                    $("#ddl_alertas").append(alerta);
                }
            }
        }
    });
}

function notificacion(){
$.ajax({
        url:"/alertas/notify",
        type:"get",
        success:function(data){
            if (data.length>0){
                for(var i=0;i<data.length;i++){
                    $("#proceso").css({'background-color':'#F5F5F5', 'color': '#7FFF00'});
                    $("#proceso").addClass('fa-3x');
                    var proceso="";
                    if(data[i].mensaje.includes("rechazada")){
                        var up="<li><a href='"+data[i].ruta+"'><div><i class='fa fa-remove fa-fw'></i>";var mid="<span class='pull-right text-muted small'>";
                        var end="</span></div></a></li>";
                        proceso=up+data[i].mensaje+mid+data[i].sub_mensaje+end+"<li class='divider'></li>"; 
                    }else{
                        var up="<li><a href='"+data[i].ruta+"'><div><i class='fa fa-check-circle-o fa-fw'></i>";var mid="<span class='pull-right text-muted small'>";
                        var end="</span></div></a></li>";
                        proceso=up+data[i].mensaje+mid+data[i].sub_mensaje+end+"<li class='divider'></li>";
                    }


                    $("#ddl_proceso").append(proceso);
                }
            }
        }
    });

}

// function despacho(){
//     $.ajax({
//         url:"/alertas/dispatch",
//         type:"get",
//         success:function(data){
//             if (data.length>0){
//                 for(var i=0;i<data.length;i++){
//                     var html='<div><i class="fa fa-comment fa-fw"></i> New Comment<span class="pull-right text-muted small">4 minutes ago</span></div>';
//                     $("#alertas").css({'background-color':'#F5F5F5', 'color': 'red'});
//                     $("#alertas").addClass('fa-3x');
//                     var up="<li><a href='"+data[i].ruta+"'><div><i class='fa fa-upload fa-fw'></i>";
//                     var mid="<span class='pull-right text-muted small'>";
//                     var end="</span></div></a></li>";
//                     var alerta=up+data[i].mensaje+mid+data[i].requiere__usuario__username+" solicita "+data[i].sub_mensaje+end+"<li class='divider'></li>";
//                     $("#ddl_alertas").append(alerta);
//                 }
//             }
//         }
//     });
// }




$(document).ready(function(){
    // asetup();
    alertas();
    notificacion();
    // despacho();
    });