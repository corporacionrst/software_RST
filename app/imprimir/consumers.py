import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session
from .tasks import cargar_a_cola


# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("cola_socket").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return
    if data:
        reply_channel = message.reply_channel.name
        if data['action'] == "agregar_productos":
            agregar_productos(data, reply_channel)
    return False


def ws_disconnect(message):
    Group("cola_socket").discard(message.reply_channel)



def agregar_productos(data,reply_channel):
	usu=data['usu']
	pagina=int(data["pagina"])
	task_id=cargar_a_cola.delay(pagina,usu,reply_channel)

