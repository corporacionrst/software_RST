
def moneda(valor):
	if valor=="Q":
		return " QUETZALES "
	elif valor=="E":
		return " EUROS "
	elif valor=="$USD":
		return " DOLARES "
	elif valor=="$MXN":
		return " PESOS MEXICANOS "
	else:
		return "_?_"

def val_a_cad(val,currency):
	ent = val.split(".")
	if len(ent)==1:
		return entero(val) +moneda(currency)+" EXACTOS"
	else:
		return entero(ent[0]) +moneda(currency)+" CON " +decimal(ent[1])
def decimal(val):
	if len(val)==1:
		val="0"+val
	elif len(val)==2:
		val=val
	else:
		s=int(val[1])+1
		val=val[0]+s
	return val+"/100"
def entero(val):
	if len(val)==9:
		return cmillon(val)
	elif len(val)==8:
		return dmillon(val)
	elif len(val)==7:
		return umillon(val)
	elif len(val)==6:
		return cemil(val)
	elif len(val)==5:
		return demil(val)
	elif len(val)==4:
		return umil(val)
	elif len(val)==3:
		return centena(val)
	elif len(val)==2:
		return decena(val)
	elif len(val)==1:
		return unidad(val)


def cmillon(val):
	cad = val[3]+""+val[4]+""+val[5]+""+val[6]+""+val[7]+""+val[2]
	return centena(val[0]+""+val[1]+""+val[2])+" MILLONES "+ cemil(cad)


def dmillon(val):
	cad = val[2]+""+val[3]+""+val[4]+""+val[5]+""+val[6]+""+val[7]
	return decena(val[0]+""+val[1])+" MILLONES "+ cemil(cad)

def umillon(val):
	cad = cemil(val[1]+""+val[2]+""+val[3]+""+val[4]+""+val[5]+""+val[6])
	if val[0]=="1":
		return "UN MILLON "+cad
	else:
		return unidad(val[0])+" MILLONES "+cemil(cad)

def cemil(val):
	return centena(val[0]+""+val[1]+""+val[2])+"MIL "+centena(val[3]+""+val[4]+""+val[5])

def demil(val):
	return decena(val[0]+""+val[1])+"MIL "+centena(val[2]+""+val[3]+""+val[4])

def umil(val):
	cen = val[1]+""+val[2]+""+val[3]
	if val[0]=="0":
		return centena(cen)
	if val[0]=="1":
		return "MIL "+centena(cen)
	else:
		return unidad(val[0])+"MIL "+centena(cen)
def centena(val):
	dec = val[1]+""+val[2]
	if val[0]=="0":
		return decena(dec)
	elif val[0]=="1":
		if val[1]=="0" and val[2]=="0":
			return "CIEN"
		else:
			return "CIENTO "+decena(dec)
	elif val[0]=="2":
		return "DOSCIENTOS "+decena(dec)
	elif val[0]=="3":
		return "TRESCIENTOS "+decena(dec)
	elif val[0]=="4":
		return "CUATOCIENTOS "+decena(dec)
	elif val[0]=="5":
		return "QUINIENTOS "+decena(dec)
	elif val[0]=="6":
		return "SEISCIENTOS "+decena(dec)
	elif val[0]=="7":
		return "SETECIENTOS "+decena(dec)
	elif val[0]=="8":
		return "OCHOCIENTOS "+decena(dec)
	elif val[0]=="9":
		return "NOVECIENTOS"+decena(dec)

def decena(val):
	if val[0]=="0":
		return unidad(val[1])
	if val[0]=="1":
		if val[1]=="0":
			return "DIEZ"
		elif val[1]=="1":
			return "ONCE"
		elif val[1]=="2":
			return "DOCE"
		elif val[1]=="3":
			return "TRECE"
		elif val[1]=="4":
			return "CATORCE"
		elif val[1]=="5":
			return "QUINCE"
		else:
			return "DIEZ Y " +unidad(val[1])
	if val[0]=="2":
		if val[1]=="0":
			return "VEINTE"
		else:
			return "VENINTI"+unidad(val[1])
	if val[0]=="3":
		if val[1]=="0":
			return "TREINTA"
		else:
			return "TREINTA Y "+unidad(val[1])
	if val[0]=="4":
		if val[1]=="0":
			return "CUARENTA "
		else:
			return "CUARENTA Y "+unidad(val[1])
	if val[0]=="5":
		if val[1]=="0":
			return "CINCUENTA"
		else:
			return "CINCUENTA Y "+unidad(val[1])
	if val[0]=="6":
		if val[1]=="0":
			return "SESENTA"
		else:
			return "SESENTA Y "+unidad(val[1])
	if val[0]=="7":
		if val[1]=="0":
			return "SETENTA"
		else:
			return "SETENTA Y "+unidad(val[1])
	if val[0]=="8":
		if val[1]=="0":
			return "OCHENTA"
		else:
			return "OCHENTA Y "+unidad(val[1])
	if val[0]=="9":
		if val[1]=="0":
			return "NOVENTA"
		else:
			return "NOVENTA Y "+unidad(val[1])

def unidad(val):
	if val=="0":
		return "CERO"
	elif val=="1":
		return "UNO"
	elif val=="2":
		return "DOS"
	elif val=="3":
		return "TRES"
	elif val=="4":
		return "CUATRO"
	elif val=="5":
		return "CINCO"
	elif val=="6":
		return "SEIS"
	elif val=="7":
		return "SIETE"
	elif val=="8":
		return "OCHO"
	elif val=="9":
		return "NUEVE"
