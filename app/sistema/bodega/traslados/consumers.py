import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session
from .tasks import solicitud_de_traslado,autoriza_traslado


def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("traslado").add(message.reply_channel)

def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return

    if data:
        reply_channel = message.reply_channel.name
        if data['action'] == "traslado":
            inter_tienda(data, reply_channel)
        elif data['action']=="auth_traslado":
            auth_traslado(data,reply_channel)


def ws_disconnect(message):
    Group("alertas").discard(message.reply_channel)



def inter_tienda(data,reply_channel):
    de=data['de']
    para=data['para']
    usuario=data['usu']
    task_id=solicitud_de_traslado(de,para,usuario,reply_channel)

def auth_traslado(data,reply_channel):
    id_=data['id']
    val=data['val']
    autoriza=data['autoriza']
    autorizada=data['autorizada']
    task_id=autoriza_traslado.delay(id_,val,autoriza,autorizada,reply_channel)
