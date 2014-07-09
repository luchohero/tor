from django import forms
from django.contrib.auth.models import User
from app.models import *
Plazo = ((True,'Si'),(False,'No'),)
class Entregaform(forms.Form):
    Usuario = forms.ModelChoiceField(queryset=Funcionario.objects.all())
    Desde = forms.IntegerField(max_value=800000,min_value=1,required=True)
    Hasta = forms.IntegerField(max_value=800000,min_value=1,required=True)
    Transferible = forms.ChoiceField(required=False,choices=Plazo)


class Entregaformsocio(forms.Form):
    Razon = forms.ModelChoiceField(queryset=Motivo.objects.all())   
    Efectivo = forms.IntegerField(max_value=500000,min_value=1,required=True)
    
class Boletosform(forms.Form):
    Desde = forms.IntegerField(max_value=800000,min_value=1)
    Hasta = forms.IntegerField(max_value=800000,min_value=1)

class Socioform(forms.Form):
    Socio = forms.IntegerField(max_value=199999999999,min_value=1)

class Negociacion(forms.Form):
    Socio = forms.IntegerField()
    boletos = forms.IntegerField()


class Negociacion1(forms.Form):
    boletos = forms.IntegerField()
    razon = forms.CharField(widget=forms.Textarea)

class Boleto1(forms.Form):
    boleto = forms.IntegerField()

class Socio1(forms.Form):
    socio = forms.IntegerField()

class Funcionario1(forms.Form):
    funcionario = forms.CharField()

