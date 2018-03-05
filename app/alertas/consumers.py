import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session

from ..sistema.administrador.administrador.views import pedir_permiso
from ..productos.inventario.orden.views import check_oc,quit_orden,ok_oc
from ..sistema.cobros.depositos.views import realizar_deposito,descartar_deposito_de_cuentas,autorizar_deposito_de_cuenta

from ..productos.inventario.historial.views import rechazo_de_impresion
# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("alertas").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return

    if data:
        reply_channel = message.reply_channel.name
        if data['action']=="pedir_permiso":
            pedir_permiso_credito(data,reply_channel)
        elif data['action'] == "cargar_orden":
            cargar_orden(data, reply_channel)
        elif data['action']=="descartar_orden":
            descartar_orden(data,reply_channel)
        elif data['action']=="autorizar_orden":
            autorizar_orden(data,reply_channel)
        elif data['action']=="alertas":
        	envia_alerta(data,reply_channel)
      	elif data['action']=="dropdown_productos":
      		productos_en_cola(data,reply_channel)
        elif data['action']=="asignar_deposito":
            asignar_deposito_entre_cuentas(data,reply_channel)
        elif data['action']=="descartar_deposito":
            descartar_deposito_cuenta(data,reply_channel)
        elif data['action']=="autorizar_deposito":
            autorizar_deposito_cuenta(data,reply_channel)
        elif data['action']=="rechazar_impresion":
            rechazar_impresion(data,reply_channel)

def ws_disconnect(message):
    Group("alertas").discard(message.reply_channel)

def rechazar_impresion(data,reply_channel):
    print "SI?"
    documento=data['documento']
    motivo=data['motivo']
    task_id=rechazo_de_impresion(documento,motivo,reply_channel)


def descartar_orden(data,reply_channel):
    no_orden=data['info']
    com=data['comentario']
    usuario=data['usuario']
    task_id=quit_orden(no_orden,com,usuario,reply_channel)

def cargar_orden(data,reply_channel):
    nnit=data['nit']
    nit=nnit.upper()
    credito=data['codigo']
    store=data['usu']
    task_id=check_oc(nit,credito,store,reply_channel)

def autorizar_orden(data,reply_channel):
    info =data['info']
    usu=data['usuario']
    task_id=ok_oc(info,usu,reply_channel)


def asignar_deposito_entre_cuentas(data,reply_channel):
    de=data['de']
    para=data['recibe']
    monto=data['monto']
    doc=data['documento']
    task_id=realizar_deposito(de,para,monto,doc,reply_channel)

def descartar_deposito_cuenta(data,reply_channel):
    no=data['info']
    task_id=descartar_deposito_de_cuentas(no,reply_channel)


def autorizar_deposito_cuenta(data,reply_channel):
    no=data['info']
    task_id=autorizar_deposito_de_cuenta(no,reply_channel)

def pedir_permiso_credito(data,reply_channel):
    usuario=data['usuario']
    task_id=pedir_permiso(usuario,reply_channel)