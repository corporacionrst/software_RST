from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from ..tienda.models import EMPRESA

class PUESTO(models.Model):
	# 1 : administrador
	# 2 : contabilidad
	# 3 : bodega
	# 4 : cobros
	# 5 : ventas
	id = models.AutoField(primary_key=True)
	nombre=models.CharField(max_length=15)
	def __unicode__(self):
		return unicode(self.nombre)
	
class Perfil(models.Model):
	# marcosmayen: marcos: mayen:z4m:administrador:central:92:92:1-MM-1:2-MM-1:3-MM-1:4-MM-1:O-MM-1:E-MM-1
	usuario = models.OneToOneField(User,default=1)
	nombre = models.CharField(max_length=50,default="usuario")
	apellido= models.CharField(max_length=50,default="apellido")
	direccion = models.CharField(max_length=200,default="direccion")
	puesto = models.ForeignKey(PUESTO,null=True)
	telefono=models.CharField(max_length=10,default="2208-1414")
	tienda = models.ForeignKey(EMPRESA)
	fecha_nacimiento= models.DateField()
	fecha_ingreso = models.DateField()
	documento4 = models.CharField(max_length=300,default="4-a-1")
	multitienda=models.BooleanField(default=False)
	cui = models.CharField(max_length=100,default="")
	ultima_indemnizacion = models.DateField()
	no_igss=models.CharField(max_length=100,default="")
	def __unicode__(self):
		return self.usuario.username

class PERMISOS(models.Model):
	Perfil=models.ForeignKey(Perfil)
	fecha=models.DateField()
	solicitud = models.CharField(max_length=300,default="vacaciones")
	motivo = models.CharField(max_length=300,default="")
	autorizado=models.BooleanField(default=False)


class SALARIO_MENSUAL (models.Model):
	usuario = models.ForeignKey(Perfil)
	fecha_de_pago = models.DateField()
	salario = models.DecimalField(max_digits=300,decimal_places=4)
	comision = models.DecimalField(max_digits=300,decimal_places=4,default=0)
	total = models.DecimalField(max_digits=300,decimal_places=4,default=0)


class USUARIO_TIENDA(models.Model):
	usuario = models.ForeignKey(Perfil,related_name="user")
	tienda = models.ForeignKey(EMPRESA,related_name="store")
	actual=models.IntegerField(default=1)
	orden= models.IntegerField(default=1)
	fac_1= models.IntegerField(default=1)
	fac_2= models.IntegerField(default=1)
	fac_3= models.IntegerField(default=1)
	fac_4= models.IntegerField(default=1)
	proforma=models.IntegerField(default=1)

class DOCUMENTO_POR_TIENDA(models.Model):
	ubicado = models.ForeignKey(USUARIO_TIENDA)
	# pagina 0=orden, pag1=fac_1, pag2=fac_2...
	pagina=models.IntegerField(default=0)
	correlativo = models.IntegerField(default=1)
	tipo_doc=models.CharField(max_length=1,default="V")
	credito=models.BooleanField(default=False)
	total = models.DecimalField(max_digits=300,decimal_places=4,default=0)
	descuento=models.DecimalField(max_digits=300,decimal_places=4,default=0)
	