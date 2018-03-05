import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session

from .tasks import crear_proveedor


def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("chat").add(message.reply_channel)


def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return

    if data:
        reply_channel = message.reply_channel.name
        if data['action'] == "crear_proveedor":
            create_provider(data, reply_channel)

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)


def create_provider(data,reply_channel):
	nit=data['nit']
	nombre=data['nombre']
	dirs=data['dirs']
	tel=data['tel']
	mail=data['mail']
	comm=data['comm']
	credit=data['credit']
	days=data['days']
	money=data['money']
	store=data['store']
	task_id=crear_proveedor.delay(nit,nombre,dirs,tel,mail,comm,credit,days,money,store,reply_channel)
    

