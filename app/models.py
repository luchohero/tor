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

class Agencia(models.Model):
	Cod = models.IntegerField(primary_key=True,max_length=5)
	Agencia = models.CharField(max_length=500)
	def __unicode__(self):
		return u'%s'%self.Agencia



class Funcionario(models.Model):
	Cod = models.IntegerField(primary_key=True,max_length=5)
	Nombres = models.CharField(max_length=500,blank=True,null=True)
	Users = models.CharField(max_length=50,blank=True,null=True)
	Agencia = models.ForeignKey(Agencia,blank=True,null=True)
	def __unicode__(self):
		return u'%s'%self.Nombres


class Boleto(models.Model):
	Numero = models.IntegerField(max_length=13,help_text='Numero de boleto', unique=True,primary_key=True)
	Socio = models.ForeignKey(Cuenta,null=True,blank=True)
	Funcionario = models.ForeignKey(Funcionario,null=True,blank=True)
	Fecha = models.DateTimeField(auto_now_add=True)
	Fecha_e = models.DateField(null=True,blank=True)
	Fecha_e_s = models.DateField(null=True,blank=True)
	Entrega = models.BooleanField()
	Motivo = models.ForeignKey(Motivo,null=True,blank=True)
	Baja = models.BooleanField(default=False)
	Transferible = models.BooleanField(default=False)
	Agencia = models.ForeignKey(Agencia,null=True, blank=True)
	
	def __unicode__(self):
		return u'%s'%self.Numero

	

class Historial(models.Model):
	Cuenta = models.ForeignKey(Cuenta)
	Monto = models.IntegerField()
	Boletos = models.IntegerField()
	Fecha = models.DateField(auto_now_add=True)



