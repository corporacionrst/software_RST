import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session
# from channels.auth import channel_session_user, channel_session_user_from_http
# from .tasks import crear_marca_task
from .tasks import crear_producto_task


# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return

    if data:
        reply_channel = message.reply_channel.name

        if data['action'] == "crear_producto":
            crear_marca(data, reply_channel)

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)


def crear_marca(data,reply_channel):
    codigo = data['codigo']
    descripcion = data['descripcion']
    marca=data['marca']
    es_set=data['set']
    no_set=data['no_set']
    task_id = crear_producto_task.delay(codigo,descripcion,marca,es_set,no_set,reply_channel)
    

