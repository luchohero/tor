# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Cuenta(models.Model):
	Numero = models.IntegerField(max_length=13)
	Fecha = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return u'%d' %self.Numero

class Motivo(models.Model):
	Razon = models.CharField(max_length=128)
	Boletos_n = models.IntegerField(max_length=13,help_text='Numero de boletos')
	Ciclo = models.IntegerField(max_length=10)
	Repetitivo =  models.BooleanField()
	def __unicode__(self):             
		return u'%s'%self.Razon


class Boleto(models.Model):
	Numero = models.IntegerField(max_length=13,help_text='Numero de boleto', unique=True,primary_key=True)
	Socio = models.ForeignKey(Cuenta,null=True,blank=True)
	Funcionario = models.ForeignKey(User,null=True,blank=True)
	Fecha = models.DateTimeField(auto_now_add=True)
	Fecha_e = models.DateField(null=True,blank=True)
	Fecha_e_s = models.DateField(null=True,blank=True)
	Entrega = models.BooleanField()
	Motivo = models.ForeignKey(Motivo,null=True,blank=True)
	baja = models.BooleanField(default=False)
	


	

class Historial(models.Model):
	Cuenta = models.ForeignKey(Cuenta)
	Monto = models.IntegerField()
	Boletos = models.IntegerField()
	Fecha = models.DateField(auto_now_add=True)



