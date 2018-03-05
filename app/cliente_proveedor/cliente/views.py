# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from ...request_session import OKconta,OKpeople,getPerfil
from django.db.models import Q
from .models import CLIENTE
from ..persona.models import PERSONA
import json

from ...productos.inventario.historial.models import LISTA_PRODUCTO
from decimal import Decimal
from ...sistema.usuarios.models import USUARIO_TIENDA,DOCUMENTO_POR_TIENDA



class descuento(TemplateView):
	def post(self,request,*args,**kwargs):
		if OKpeople(request):
			try:
				indice = int(request.POST['pag'])
				if indice>0 and indice<5:
					usu = getPerfil(request)
					ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
					if ut.exists():
						ut=ut[0]
						correlativo=0
						if indice==1:
							correlativo=ut.fac_1
						elif indice==2:
							correlativo=ut.fac_2
						elif indice==3:
							correlativo=ut.fac_3
						else:
							correlativo=ut.fac_4
						dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=indice).filter(correlativo=correlativo).filter(tipo_doc="V")
						if dpt.exists():
							dpt=dpt[0]
							total=Decimal(dpt.total)*Decimal(0.95)
							dpt.descuento=total
							dpt.save()
							total = str(total).split('.')
							if len(total)==1:
								vac=total+".00"
							else:
								if len(total[1])>3:
									vac=total[0]+'.'+total[1][0]+total[1][1]+total[1][2]
								else:
									vac=total[0]+'.'+total[1]
							return HttpResponse("Aplicado, valor a cancelar:"+vac,content_type='text')
			except:
				return HttpResponse("El descuento no pudo ser aplicado",content_type='text')
		return HttpResponse("El descuento no pudo ser aplicado",content_type='text')




class mayorista(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			nit = request.GET["nit"]
			pag = int(request.GET["pagina"])
			credito = request.GET['credito']
			if pag>0 and pag<5:
				usu = getPerfil(request)
				ppl =PERSONA.objects.get(nit=nit)
				cl =CLIENTE.objects.filter(info=ppl).filter(store=usu.tienda)
				ut = USUARIO_TIENDA.objects.filter(usuario=usu).filter(tienda=usu.tienda)
				if cl.exists() and ut.exists():
					ut=ut[0]
					cl=cl[0]
					correlativo=0
					if pag==1:
						correlativo=ut.fac_1
					elif pag==2:
						correlativo=ut.fac_2
					elif pag==3:
						correlativo=ut.fac_3
					else:
						correlativo=ut.fac_4
					dpt = DOCUMENTO_POR_TIENDA.objects.filter(ubicado=ut).filter(pagina=pag).filter(correlativo=correlativo).filter(tipo_doc="V")
					if dpt.exists():
						dpt=dpt[0]
						if dpt.total!=0:
							if ((cl.credito==True) and ("true" in credito) and (cl.monto>0)):
								total=dpt.total
								if cl.saldo+total<=cl.monto and cl.mayorista:
									return HttpResponse("Este usuario es MAYORISTA, ¿aplicar descuento?",content_type='text')
								else:
									return HttpResponse("Su credito ha sido excedido, ¿solicitar PERMISO?(avisar al cliente)",content_type='text')
							else:
								return HttpResponse("Contado",content_type='text')
						else:
							return HttpResponse("el documento NO posee informacion");

					else:
						return HttpResponse("el documento NO posee informacion",content_type="text")
				else:
					return HttpResponse("Por favor ingrese un nit NO es valido verifique sus datos",content_type="text")
				
		return HttpResponse("el documento NO posee informacion",content_type='text')	



class ver_clientes(TemplateView):
	template_name="cliente_proveedor/cliente/cliente.html"
	def get(self,request,*args,**kwargs):
		context={}
		return render(request,self.template_name,context)


class crearCliente(TemplateView):
	def get(self,request,*args,**kwargs):
		nit = request.GET['nit']
		nombre= request.GET['nombre']
		direccion = request.GET['direccion']


class consultar_cliente_nit(TemplateView):
	def get(self,request,*args,**kwargs):
		try:
			if OKpeople(request):
				tienda=getPerfil(request).tienda
				nit = request.GET['nit'].upper()
				persona = PERSONA.objects.get(nit=nit)
				qs = CLIENTE.objects.filter(info=persona).filter(store=tienda)
				if qs.exists():
					qs=qs.values('info__nit','info__nombre','info__direccion','credito')
					qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
					return HttpResponse(qs,content_type='application/json')
			return HttpResponse("{}",content_type='application/json')
		except:
			return HttpResponse("{}",content_type='application/json')	
		return HttpResponse("{}",content_type='application/json')





class consultar_cliente_nombre(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			tienda=getPerfil(request).tienda
			nombre = request.GET['nombre']
			i=int(request.GET['pag'])*3
			qs = CLIENTE.objects.filter(Q(info__nombre__icontains=nombre)).filter(store=tienda).values('info__nit','info__nombre')[i:i+2]
			qs=json.dumps(list(qs),cls=DjangoJSONEncoder)
			return HttpResponse(qs,content_type='application/json')
		return HttpResponse("{}",content_type='application/json')



class registrar_cliente(TemplateView):
	def get(self,request,*args,**kwargs):
		if OKpeople(request):
			nit=request.GET["nit"]
			comentario=request.GET["comentario"]
			credito=request.GET["credito"]
			monto=request.GET["monto"]
			dias=request.GET["dias"]
			persona = PERSONA.objects.filter(nit=nit)
			if persona.exists():
				pr = CLIENTE.objects.filter(nit=persona)
				if pr.exists():
					return HttpResponse("-1",content_type='text')
			else:
				nombre=request.GET["nombre"]
				direccion=request.GET["direccion"]
				telefono=request.GET["telefono"]
				correo=request.GET["correo"]
				persona=PERSONA()
				persona.nit = nit
				persona.nombre= nombre
				persona.direccion =direccion
				persona.telefono = telefono
				persona.correo =correo
				persona.save()
			pr = CLIENTE()
			pr.info=persona
			pr.comentario=comentario
			pr.credito=credito
			pr.monto=monto
			pr.dias_credito=dias
			pr.save()
			HttpResponse(nit+" fue creado satisfactoriamente",content_type='text')
		return HttpResponse("-1",content_type='text')

