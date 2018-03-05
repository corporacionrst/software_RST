from decimal import Decimal
def distribuidor(antiguo,nuevo):
	antiguo=float(antiguo)
	nuevo=float(nuevo)
	return Decimal(max(antiguo,nuevo*1.5))

def mayorista(antiguo,nuevo):
	antiguo=float(antiguo)
	nuevo=float(nuevo)
	return Decimal(max(antiguo,nuevo*2))

def efectivo(antiguo,nuevo):
	antiguo=float(antiguo)
	nuevo=float(nuevo)
	return Decimal(max(antiguo,nuevo*3))

def tarjeta(antiguo,nuevo):
	antiguo=float(antiguo)
	nuevo=float(nuevo)
	return Decimal(max(antiguo,nuevo*4))

def l_distribuidor(antiguo,nuevo):
	antiguo=float(antiguo)
	nuevo=float(nuevo)
	return Decimal(max(antiguo,nuevo*1.15))



def l_efectivo(antiguo,nuevo):
	antiguo=float(antiguo)
	nuevo=float(nuevo)
	return Decimal(max(antiguo,nuevo*1.5))

def l_precio(antiguo,nuevo):
	antiguo=float(antiguo)
	nuevo=float(nuevo)
	return Decimal(max(antiguo,nuevo*1.8))

def iva(valor):
	antiguo=float(antiguo)
	nuevo=float(nuevo)
	return Decimal(valor/1.12)
