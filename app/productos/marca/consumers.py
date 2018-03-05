import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session
# from channels.auth import channel_session_user, channel_session_user_from_http
from .tasks import crear_marca_task



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

        if data['action'] == "crear_marca":
            crear_marca(data, reply_channel)
    return False

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)


def crear_marca(data,reply_channel):
    name = data['nombre']
    importacion=data['importacion']
    pr= name+str(importacion) 
    task_id=crear_marca_task.delay(name,importacion,reply_channel)

