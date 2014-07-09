# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib import admin
from models import *
import csv
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
export_as_csv.short_description = "Export selected objects as csv file"

#Datos.objects.order_by('id',)

class Cuenta_Admin(admin.ModelAdmin):
	list_display = 'Numero','Fecha'
	list_filter =  'Numero','Fecha'
	search_fields = 'Numero',

class Boleto_Admin(admin.ModelAdmin):

	list_display = 'Numero','Fecha','Socio','Funcionario','Fecha_e','Fecha_e_s','Entrega','Motivo','Baja','Transferible','Agencia'
	list_filter = 'Funcionario','Socio','Entrega'
	search_fields = ['Numero',]

class Motivo_Admin(admin.ModelAdmin):
	list_display = 'Razon','Boletos_n','Ciclo','Repetitivo'
	list_filter = 'Razon','Boletos_n','Ciclo'
	search_fields = 'Razon','Boletos_n','Ciclo'

class Historial_Admin(admin.ModelAdmin):
	list_display = 'id','Cuenta','Monto','Boletos','Fecha'
	list_filter = 'Cuenta','Monto','Boletos','Fecha'
	search_fields = 'Cuenta','Monto','Boletos','Fecha'
	

class Agencia_Admin(admin.ModelAdmin):
    list_display = 'Cod','Agencia'
    list_filter = 'Cod','Agencia'
    search_fields = 'Cod','Agencia'

class Funcionario_Admin(admin.ModelAdmin):
    list_display = 'Cod','Nombres','Users','Agencia'
    list_filter = 'Cod','Nombres','Users','Agencia'
    search_fields = 'Cod','Nombres','Users','Agencia'   




admin.site.register(Cuenta, Cuenta_Admin)
admin.site.register(Boleto, Boleto_Admin)
admin.site.register(Motivo, Motivo_Admin)
admin.site.register(Agencia, Agencia_Admin)
admin.site.register(Funcionario, Funcionario_Admin)
admin.site.register(Historial, Historial_Admin)



