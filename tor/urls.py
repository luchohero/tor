from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.Home', name='Home'),
    url(r'^login/$', 'app.views.Ingresar',),
    url(r'^entrega/$', 'app.views.Entrega',),
    url(r'^salir/$', 'app.views.Salir',),
    url(r'^excel/$', 'app.views.xls',),
    url(r'^entrega-socio/$', 'app.views.EntregaSocio',),
    url(r'^entrega-socio/(\d+)/$', 'app.views.EntregaSocio1',),
    url(r'^entrega-socio2/(\d+)/$', 'app.views.EntregaSocio2',),
    url(r'^entrega-socio3/(\d+)/$', 'app.views.EntregaSocio3',),
    ###
    url(r'^econx/(\d+)/(\d+)/$', 'app.views.econx',),
    #url(r'^econx-negociacion/(\d+)/(\s+)/$', 'app.views.econxnegociacion',),
    ###
    url(r'^negocio/$', 'app.views.Negocio',),
    url(r'^negocio1/(\d+)/(\d+)/$', 'app.views.Negocio',),
    # url(r'^blog/', include('blog.urls')),
    url(r'^entrega-boletos/(\d+)/(\d+)/(\d+)/$', 'app.views.EntregaBoletos'),
    url(r'^entrega-boletos/(\d+)/(\d+)/$', 'app.views.EntregaBoletos1'),
    url(r'^admin/', include(admin.site.urls)),

)
