import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session
# from channels.auth import channel_session_user, channel_session_user_from_http
from .tasks import consulta_usuario_fecha



# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("usuarios").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return

    if data:
        reply_channel = message.reply_channel.name

        if data['action'] == "fecha_de_salario":
            consulta_por_fecha(data, reply_channel)
    return False

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("usuarios").discard(message.reply_channel)


def consulta_por_fecha(data,reply_channel):
    desde = data['desde']
    if desde==None:
    	desde=""
    hasta =data['hasta']
    if hasta==None:
    	hasta=""
    usuario=data['usuario']
    task_id=consulta_usuario_fecha.delay(desde,hasta,usuario,reply_channel)

