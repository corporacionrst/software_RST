

$("#asignar_deposito").on("click", function(event) {
    var de = $('#id_de').val();
    var para=$("#id_para").val();

    var monto=document.getElementById("monto").value;
    if (monto==null || monto=="" || monto==0){
        alert("por favor ingrese un monto valido");
    }else {
        var message={
            action:"asignar_deposito",
            de:de,
            recibe:para,
            monto:monto,
            documento:document.getElementById('documento').value,
        };
        alert_socket.send(JSON.stringify(message));
        alert("usuario avisado");
        return true;
    }
    return false;

});

