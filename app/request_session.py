from sistema.usuarios.models import Perfil

def getPerfil(request):
	return Perfil.objects.get(usuario=request.user)

# def getStore(request):
# 	return Perfil.objects.get(usuario=request.user).tienda
		

def OKadmin(request):
	if request.user.is_authenticated():
		if "ADMIN" in Perfil.objects.get(usuario=request.user).puesto.nombre:
			return True
	return False

def OKbodega(request):
	if request.user.is_authenticated():
		ppl=Perfil.objects.get(usuario=request.user).puesto.nombre
		if "BODEGA" in ppl:
			return True
		elif "ADMIN" in ppl:
			return True
	return False

def OKconta(request):
	if request.user.is_authenticated():
		ppl=Perfil.objects.get(usuario=request.user).puesto.nombre
		if "CONTA" in ppl:
			return True
		elif "ADMIN" in ppl:
			return True
	return False

def OKmultitienda(request):
	if request.user.is_authenticated():
		return Perfil.objects.get(usuario=request.user).multitienda
	return False

def OKcobros(request):
	if request.user.is_authenticated():
		ppl=Perfil.objects.get(usuario=request.user).puesto.nombre
		if "COBROS" in ppl or "ADMIN" in ppl:
			return True
	return False

def OKventas(request):
	if request.user.is_authenticated():
		ppl=Perfil.objects.get(usuario=request.user).puesto.nombre
		if "VENTA" in ppl:
			return True
		elif "ADMIN" in ppl:
			return True
	return False

def OKpeople(request):
	if request.user.is_authenticated():
		return True
	return False

def sumar_DATO(request,numero):
	val=Perfil.objects.get(usuario=request.user)
	if numero=="4":
		v = val.documento4.split("~")
		val.documento4=v[0]+"~"+v[1]+"~"+str(int(v[2])+1)
	
	val.save()
	return v[0]+"~"+v[1]+"~"+str(int(v[2])+1)

def obtenerPlantilla(request):
	if OKadmin(request):
		return "admin.html"
	elif OKconta(request):
		return "conta.html"
	elif OKbodega(request):
		return "bodega.html"
	elif OKcobros(request):
		return "cobros.html"
	else:
		return "ventas.html"
	