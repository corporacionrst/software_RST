

$("#cargar_orden").on("click", function(event) {
    var nit = document.getElementById("id_nit").value;
    var credito=document.getElementById("id_credito").checked;
    if (nit==null || nit==""){
        alert("por favor ingrese el numero de nit");
    }else {
        var message={
            action:"cargar_orden",
            nit:nit,
            usu:usuario,
            codigo:credito
        };
        alert_socket.send(JSON.stringify(message));
        window.location.reload();

    }
    return true;

});

