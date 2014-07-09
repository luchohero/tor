# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from app.models import *
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from app.forms import *
from django.contrib.auth.models import *
import datetime
######## Libreria XlS #########
import xlwt

# Create your views here.

@login_required(login_url='/login/')
def Home(request):
	usuario = request.user

	
	return render_to_response('inicio.html',{'usuario':usuario},
		context_instance=RequestContext(request))

def Ingresar(request):

  if not request.user.is_anonymous():
        return HttpResponseRedirect('/manage/')
  if request.method == 'POST':
    formulario_ing = AuthenticationForm(request.POST)
    if formulario_ing.is_valid:
      usuario = request.POST['username']
      clave = request.POST['password']
      acceso = authenticate(username=usuario, password=clave)
      if acceso is not None:
        if acceso.is_active:
          login(request, acceso)
          return HttpResponseRedirect('/')
        else:
          mensaje = 'error'
          return HttpResponseRedirect('')
      else:
        mensaje = 'error1'
        return HttpResponseRedirect('')
  else:
    formulario_ing = AuthenticationForm()
  return render_to_response('acceso.html',{'formulario_ing':formulario_ing}, 
  	context_instance=RequestContext(request))

###############Entrega Funcionario #################
def Entrega(request):
	Valores = 'Valores: '
	if request.method == 'POST':
		#if not request.POST['Desde'] or request.POST['Hasta']:
		#	return HttpResponseRedirect('/entrega/')
		formulario_post = Entregaform(request.POST)

		if formulario_post.is_valid:

			u = request.POST['Desde']
			Desde = int(u)
			u1 = request.POST['Hasta']
			Hasta = int(u1)
			print request.POST['Usuario']
			usuario = Funcionario.objects.get(Cod=request.POST['Usuario'])
			for q in range(Desde,Hasta+1):
				print q
			#log entrega al usuario
			#print Boleto.objects.all().get(Numero=q)
				if not Boleto.objects.all().filter(Numero=q):
					
					ing = Boleto.objects.create(
							Numero=q,Funcionario=usuario,Fecha_e=datetime.date.today(),
							Entrega=False,Transferible=request.POST['Transferible'])
					
				
				else:
					Valores = '%s | %s |' %(Valores,q)
			if 	Valores != 'Valores: ':
				Html = """<!DOCTYPE html><html><head><title>Ingreso</title>
				<link type='text/css' rel='stylesheet' href='/static/css/base.css' />
				<link type='text/css' rel='stylesheet' href='/static/css/bootstrap.css' />
				</head><body><p>Se Dectectaron Errores en: %s</p> <br> 
				<a href='/salir/' class='btn'>SALIR</a>
				</body></html> """ %(Valores)	
				return HttpResponse(Html)	
		else:
			return HttpResponse('funciona')		
			#e = e + int(q)
		#	diferencia = request.POST['desde'] - request.POST['hasta']
		#	print diferencia
		#	return HttpResponseRedirect('/')
		
	else:
		#return HttpResponse('hola')
		formulario = Entregaform()
		return render_to_response('entrega.html',{'formulario':formulario}, 
				context_instance=RequestContext(request))
	return HttpResponseRedirect('/salir/')
	
############### Entrega al Socio #################
def EntregaSocio(request):
	if request.method == 'POST':
		
		if len(request.POST['Socio']) == 0:


			formulario = Socioform()


			texto = '<div class="alert alert-error">Por favor ingrese un valor</div>'

			return render_to_response('entrega1.html',{'formulario':formulario,'texto':texto},
					context_instance=RequestContext(request))

			
		else:
			

			if Cuenta.objects.all().filter(Numero=request.POST['Socio']):
				s = request.POST['Socio']
				return HttpResponseRedirect('%s'%s)

			else:
				s = request.POST['Socio']
				ing = Cuenta.objects.create(Numero=request.POST['Socio'])
				return HttpResponseRedirect('%s'%s)
	else:
		formulario = Socioform()
		return render_to_response('entrega1.html',{'formulario':formulario}, 
		context_instance=RequestContext(request))
				
def EntregaSocio1(request,cuenta,usuario):
	if Cuenta.objects.all().filter(Numero=cuenta):

		if request.method == 'POST':
			
			
			c = Cuenta.objects.get(Numero=cuenta)
			############ no basio #################
			if len(request.POST['Razon'])== 0:
				formulario = Entregaformsocio()
				return render_to_response('entrega1.html',{'formulario':formulario}, 
					context_instance=RequestContext(request))
			if len(request.POST['Efectivo']) == 0:
				formulario = Entregaformsocio()
				return render_to_response('entrega1.html',{'formulario':formulario}, 
					context_instance=RequestContext(request))
		#######################################
			t = Motivo.objects.get(id=request.POST['Razon']) 
			if t.Repetitivo == False:
				razon = request.POST['Razon']
				e = Motivo.objects.get(id=razon)
				b = request.POST['Efectivo']
				b1 = int(b)
				
				f = b1 / e.Ciclo
				socio = c.id
				###>>>>>>> historial
				
				l = Historial.objects.create(Cuenta=c,Monto=0,Boletos=1)
				cadena = '/entrega-boletos/%s/1/%s/%s' %(socio,razon,usuario)
				return HttpResponseRedirect(cadena)
			else:
				razon = request.POST['Razon']
				e = Motivo.objects.get(id=razon)
				b = request.POST['Efectivo']
				b1 = int(b)
				
				f = b1 / e.Ciclo
				socio = c.id
				###>>>>>>> historial
				
				l = Historial.objects.create(Cuenta=c,Monto=0,Boletos=f)
				cadena = '/entrega-boletos/%s/%s/%s/%s' %(socio,f,razon,usuario)
				return HttpResponseRedirect(cadena)


	formulario = Entregaformsocio()
	return render_to_response('entrega1.html',{'formulario':formulario}, 
	context_instance=RequestContext(request))
	
def EntregaSocio2(request,s):
	if Cuenta.objects.all().filter(Numero=s):
		pass	
	else:	
		ing = Cuenta.objects.create(
			Numero=s)
	if request.method == 'POST':
		
			############ no basio #################
		if len(request.POST['Razon'])== 0:
			formulario = Entregaformsocio()
			return render_to_response('entrega1.html',{'formulario':formulario}, 
					context_instance=RequestContext(request))
		if len(request.POST['Efectivo']) == 0:
			formulario = Entregaformsocio()
			return render_to_response('entrega1.html',{'formulario':formulario}, 
					context_instance=RequestContext(request))
		#######################################

		razon = request.POST['Razon']
		e = Motivo.objects.get(id=razon)
		b = request.POST['Efectivo']
		b1 = int(b)
		print b1
		print e.Ciclo
		f = b1 / e.Ciclo
		socio = Cuenta.objects.get(Numero=s)
		socio = socio.id
		cadena = '/entrega-boletos/%s/%s/%s' %(socio,f,razon)
		return HttpResponseRedirect(cadena)


	formulario = Entregaformsocio()
	return render_to_response('entrega1.html',{'formulario':formulario}, 
		context_instance=RequestContext(request))

def EntregaSocio3(request,s,b):

	cadena = '/entrega-boletos/%s/%s/' %(socio,f)
	return HttpResponseRedirect(cadena)

#def EntregaSocio(request):
#	
#	if request.method == 'POST':
#
#		############ no basio #################
#		if len(request.POST['Razon'])== 0:
#			return HttpResponse('d')
#		if len(request.POST['Socio']) == 0:
#			return HttpResponse('d')
#		if len(request.POST['Efectivo']) == 0:
#			return HttpResponse('d')
#		#######################################
#
#		razon = request.POST['Razon']
#		e = Motivo.objects.get(id=razon)
#		b = request.POST['Efectivo']
#		b1 = int(b)
#		print b1
#		print e.Ciclo
#		f = b1 / e.Ciclo
#		socio = request.POST['Socio']
#		print f
#		cadena = '/entrega-boletos/%s/%s/%s' %(socio,f,razon)
#		return HttpResponseRedirect(cadena)
	
#	return HttpResponseRedirect('/entrega-socio/')

################ Boletos #######################

def EntregaBoletos(request,s,b,m,usuario):

	if Cuenta.objects.all().filter(Numero=s):
		pass	
	else:	
		ing = Cuenta.objects.create(
			Numero=s)
	socio = Cuenta.objects.get(id=s)
	
	if request.method == 'POST':
		u = request.POST['Desde']
		Desde = int(u)
		u1 = request.POST['Hasta']
		Hasta = int(u1)
		if Desde>Hasta:
			return HttpResponse('error')
		if Hasta-Desde >= int(b):
			return HttpResponse('te recordamos que solo deben ser %s Boletos <a href="/salir/">salir</a>' %b) 
		
		m1 = Motivo.objects.get(id=m)

			#### dos filtros previos #### 
			# 1 si el usuario tiene permiso sobre los numeros
			# 2 si el boleto no esta marcado aun
		
		g = Funcionario.objects.get(Cod=usuario)

		if m1.Repetitivo == False:
				#si el boleto no es del usuario
				
				######################################
			ing = Boleto.objects.get(Numero=Desde)

				

			if ing.Entrega == False:
				ing.Socio = socio
				ing.Motivo = m1
				ing.Fecha_e_s = datetime.date.today()
				ing.Entrega = True
				ing.Funcionario = g
				ing.save()
				
				html = """<h1>Se realizo con exito 
						<a href="/salir/">Salir</a></h1>"""
				return HttpResponse(html)
			else:
				formulario = Boletosform()
				cadena = '/entrega-boletos/%s/1/%s' %(s,m)
				return HttpResponseRedirect(cadena)
				#if ing.Funcionario != request.user:
				#	return HttpResponse('este registro no es tuyo')
			#variable que regresa con los boletos ya entregados
		v = 0	
		j = 0
		for q in range(Desde,Hasta+1):

				#log entrega alsocio
			U = ' %s' %(datetime.date.today())
				#Guardo los datos de entrega del socio
			ing = Boleto.objects.get(Numero=q)
				
			if ing.Entrega == False:
				ing.Socio = socio
				ing.Motivo = m1
				ing.Fecha_e_s = datetime.date.today()
				ing.Entrega = True
				ing.Funcionario = g
				ing.save()
				v += 1
			else:
				j += 1
				print j
				#tomar encuenta errores y tambien el numero de voletos previo ingreso
		
		valor = int(b) - v

		
		if valor == 0: 
			html = """<h1>Se realizo con exito 
			<a href="/salir/">Salir</a></h1>"""
			return HttpResponse(html)
			
		else:

			formulario = Boletosform()
			cadena = '/entrega-boletos/%s/%s/%s/%s' %(s,valor,m,usuario)
			return HttpResponseRedirect(cadena)
			
	else:
		d = Historial.objects.all().filter(Cuenta=socio)
		formulario = Boletosform()
		html = '<span class="label label-success">Debe entregar  %s Boletos</span>' %(b)
		return render_to_response('entrega.html',{'formulario':formulario,'html':html,'d':d}, 
				context_instance=RequestContext(request))

def EntregaBoletos1(request,s,b,usuario):

	if Cuenta.objects.all().filter(Numero=s):
		pass	
	else:	
		ing = Cuenta.objects.create(
			Numero=s)
	socio = Cuenta.objects.get(Numero=s)
	
	if request.method == 'POST':
		u = request.POST['Desde']
		Desde = int(u)
		u1 = request.POST['Hasta']
		Hasta = int(u1)
		if Desde>Hasta:
			return HttpResponse("""<p>Tenemos un Error por favor comunicar al Administrador  </p>
				<a href="/salir/">salir</a>""")
		if Hasta-Desde >= int(b):
			return HttpResponse('te recordamos que solo deben ser %s Boletos <a href="/salir/">salir</a>' %b) 
		v = 0	
		us = Funcionario.objects.get(Cod=usuario)
		j = 0
		for q in range(Desde,Hasta+1):

				#log entrega alsocio
			U = ' %s' %(datetime.date.today())
				#Guardo los datos de entrega del socio
			if not Boleto.objects.all().filter(Numero=q):
				return HttpResponse('error un boleto ingresado no esta en el sistema <a href="/salir/">salir</a>')
			ing = Boleto.objects.get(Numero=q)
				
			if ing.Entrega == False:
				ing.Socio = socio
				ing.Funcionario = us
				ing.Fecha_e_s = datetime.date.today()
				ing.Entrega = True
				ing.save()
				v += 1
			else:
				j += 1
				print j
				#tomar encuenta errores y tambien el numero de voletos previo ingreso
		
		valor = int(b) - v

		
		if valor == 0: 
			return HttpResponseRedirect('/salir/')
			
		else:

			formulario = Boletosform()
			cadena = '/entrega-boletos/%s/%s/%s' %(s,valor,socio)
			return HttpResponseRedirect(cadena)
			
	else:
		d = Historial.objects.all().filter(Cuenta=socio)
		formulario = Boletosform()
		html = '<span class="label label-success">Debe entregar  %s Boletos</span>' %(b)
		return render_to_response('entrega.html',{'formulario':formulario,'html':html,'d':d}, 
				context_instance=RequestContext(request))



def Salir(request):
	return HttpResponse('<script language="javascript">setTimeout("self.close();",0)</script>')

def xls(request):
	response = HttpResponse(mimetype="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=Reporte.xls'
	usuario = request.user
	#importante codificacion
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Hoja')
	q = 2
	e = 1
    
    
	g = Boleto.objects.all().filter(Funcionario=usuario)
    
	for r in g:
		e += 1
		style_string = ""
		style = xlwt.easyxf(style_string)
		ws.write(e, 1, r.Numero,style)
		ws.write(e, 2, '%s' %(r.Socio),style)
		ws.write(e, 3, '%s' %(r.Funcionario),style)
		ws.write(e, 4, '%s' %r.Motivo,style)

	ws.write(1,1,'#')
	ws.write(1,2,'Socio')
	ws.write(1,3,'Funcionario')
	ws.write(1,4,'Motivo')
	#ws.write(1,4,'Valor')
	#ws.write(q+3,3,'TOTAL')
	#ws.write(q+3,4,e)
	wb.save(response)
	return response

def Negocio(request):
	if request.method == 'POST':
		if len(request.POST['Socio'])==0 or len(request.POST['boletos'])==0:
			formulario = Negociacion()
			html = '<div class="alert">Los campos no pueden estar basios</div>'
			return render_to_response('entrega1.html',{'formulario':formulario,'html':html}, 
				context_instance=RequestContext(request))
		if Cuenta.objects.all().filter(Numero=request.POST['Socio']):

			usuario = Cuenta.objects.get(Numero=request.POST['Socio'])
			boletos = request.POST['boletos']
			
		else:
			ing = Cuenta.objects.create(
				Numero=request.POST['Socio'])

		usuario = Cuenta.objects.get(Numero=request.POST['Socio'])

		boletos = request.POST['boletos']
		l = Historial.objects.create(Cuenta=usuario,Monto=0,Boletos=boletos)
		cadena = '/entrega-boletos/%s/%s/'%(usuario,boletos)
		return HttpResponseRedirect(cadena)
	else:
		
		formulario = Negociacion()
			
		return render_to_response('entrega1.html',{'formulario':formulario}, 
				context_instance=RequestContext(request))

def econx(request,socio,usuario):
	if Cuenta.objects.all().filter(Numero=socio):
		pass	
	else:	
		ing = Cuenta.objects.create(
			Numero=socio)
	if Funcionario.objects.all().filter(Cod=usuario):
		pass	
	else:	
		ing1 = Funcionario.objects.create(
			Cod=usuario)

	return HttpResponseRedirect('/entrega-socio/%s/%s' %(socio,usuario))

def econxnegociacion(request,socio,usuario):
	if Cuenta.objects.all().filter(Numero=socio):
		pass	
	else:	
		ing = Cuenta.objects.create(
			Numero=socio)

	return HttpResponseRedirect('/entrega-socio/%s/?usuario=%s' %(socio,usuario))

	

def Negocio(request,socio,usuario):
	if Funcionario.objects.all().filter(Cod=usuario):
		pass	
	else:	
		ing1 = Funcionario.objects.create(
				Cod=usuario)
	if request.method == 'POST':
		if len(request.POST['razon'])==0 or len(request.POST['boletos'])==0:
			formulario = Negociacion1()
			html = '<div class="alert">Los campos no pueden estar basios</div>'
			return render_to_response('entrega1.html',{'formulario':formulario,'html':html}, 
				context_instance=RequestContext(request))


		if Cuenta.objects.all().filter(Numero=socio):

			cuenta = Cuenta.objects.get(Numero=socio)
			boletos = request.POST['boletos']
			
		else:
			ing = Cuenta.objects.create(
				Numero=socio)
		

		cuenta = Cuenta.objects.get(Numero=socio)

		boletos = request.POST['boletos']
		l = Historial.objects.create(Cuenta=cuenta,Monto=0,Boletos=boletos)
		cadena = '/entrega-boletos/%s/%s/%s'%(cuenta,boletos,usuario)
		return HttpResponseRedirect(cadena)
	else:
		
		formulario = Negociacion1()
			
		return render_to_response('negocio.html',{'formulario':formulario}, 
				context_instance=RequestContext(request))
############################################
#####   Reporte  ####  Boleto ##############
def Reporte_Boleto(request):
	if request.method == 'POST':
		if Boleto.objects.all().filter(Numero=request.POST['boleto']):
			f = Boleto.objects.get(Numero=request.POST['boleto'])
			return HttpResponse("""
				<h1>Este Boleto ya fue entregado</h1>
				<p># : %s <br> al socio: %s <br> por:  %s <br> fecha: %s</p>
				<a href="/salir/">Salir</a>
				"""%(f.Numero,f.Socio,f.Funcionario,f.Fecha_e_s)) 
	else:
		formulario = Boleto1()
			
		return render_to_response('reporte_boleto.html',{'formulario':formulario}, 
				context_instance=RequestContext(request))

#####   Reporte  ####  Socio ##############

def Reporte_Funcionario(request):
	if request.method == 'POST':
		h = request.POST['funcionario']
		if Funcionario.objects.all().filter(Users=h):
			f = Funcionario.objects.all().filter(Users=request.POST['funcionario'])
			g = len(f)
			return HttpResponse("""
				<h1>Reporte</h1>
				<p>El usuario: %s <br> Entrego: %s Boletos</p>
				<a href="/salir/">Salir</a>
				"""%(request.POST['funcionario'],g)) 
	else:
		formulario = Funcionario1()
			
		return render_to_response('reporte_funcionario.html',{'formulario':formulario}, 
				context_instance=RequestContext(request))
	return HttpResponse(""" 



		""")
