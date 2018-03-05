from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from software_RST.settings.celery import app
from channels import Group
from channels import Channel

from .models import HISTORIAL,RECHAZO_IMPRESION
import datetime
from datetime import date, timedelta
@app.task
def rechazar_impresion(documento,motivo,reply_channel):
	his = HISTORIAL.objects.get(id=documento)
	ri = RECHAZO_IMPRESION()
	print datetime.date.today()+timedelta(days=3)
	
