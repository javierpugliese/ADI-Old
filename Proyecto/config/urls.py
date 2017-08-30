from django.conf.urls import url
from django.contrib import *
from adi.views import *
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #URL para carga de Template.

    url(r'^menu/$', inicio),
    url(r'^$', auth_views.login, {'template_name': 'login.html'}, name="login_p"),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name="logout_p"),
    url(r'^preceptor/$', preceptor, name="cambio"),
    url(r'^f2/$', f2, name="f2"),
    url(r'^guardia/$', guardia, name="cambio2"),
    url(r'^crearpreceptor/$', cpreceptor, name="cambio4"),
    url(r'^crearalumno/$', calumno, name="cambio5"),
    url(r'^cambiaralumno/$', chalumno, name="cambio6"),


    #URL para pasar ID.

    url(r'^presente/(\d+)$', presente, name="presente"),
    url(r'^retiro/(\d+)$', retiro_grupal, name="retiro_grupal"),
    url(r'^crear_f2/(\d+)$', crear_f2, name="crear_f2"),
    url(r'^aceptar_f3/(\d+)$', aceptar_f3, name="aceptar_f3"),
    url(r'^aceptar_f2/(\d+)$', aceptar_f2, name="aceptar_f2"),
    url(r'^rechazar_f2/(\d+)$', rechazar_f2, name="rechazar_f2"),
    url(r'^rechazar_f3/(\d+)$', rechazar_f3, name="rechazar_f3"),
    url(r'^datos_alumnos/(\d+)$', datos_alumnos, name="datos_alumnos"),
    url(r'^datos_f2/(\d+)$', datos_f2, name="datos_f2"),
    url(r'^datos_f3/(\d+)$', datos_f3, name="datos_f3"),
    url(r'^volver/(\d+)$', volver, name="volver"),


    #URL de funciones sin ID.
    url(r'^crear_f2/$', crear_f2, name="crear_f2"),
    url(r'^crearf3/$', crear_formulario3, name="crear_formulario3"),
    url(r'^crearal/$', crear_alumno, name="crear_alumno"),
    url(r'^crear_preceptor/$', crear_preceptor, name="crear_preceptor"),
    url(r'^modal/$', modificar_alumno, name="modificar_alumno"),
    url(r'^busal/$', buscar_alumno, name="buscar_alumno"),

    #URL de cargra de Templates con filtros.

    url(r'^formularios/$', formularios, name="formularios"),
    url(r'^aux_f2/$', aux_f2, name="aux_f2"),
    url(r'^f2grupal/$', f2grupal, name="f2grupal"),
    url(r'^mis_alumnos/$', mis_alumnos, name="mis_alumnos"),
]
