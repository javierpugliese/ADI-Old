from django.conf.urls import url
from django.contrib import *
from adi.views import *
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #URL para carga de Template.

    url(r'^menu/$', inicio),
    url(r'^$', index, name="index"),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name="login_p"),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name="logout_p"),
    url(r'^index_guardia/$', index_guardia, name="index_guardia"),
    url(r'^preceptor/$', preceptor, name="cambio"),
    url(r'^guardia/$', guardia, name="cambio2"),
    url(r'^prueba/estoy/$', prueba, name="prueba"),
    url(r'^crearpreceptor/$', cpreceptor, name="cambio4"),
    url(r'^crearalumno/$', calumno, name="cambio5"),
    url(r'^cambiaralumno/$', chalumno, name="cambio6"),

    #URL para pasar ID.
    url(r'^buscar_alumno/(\d+)$', buscar_alumno, name="buscar_alumno"),
    url(r'^crear_fm/(\d+)$', crear_fm, name="crear_fm"),
    url(r'^crear_f1/(\d+)$', crear_f1, name="crear_f1"),
    url(r'^crear_f2/(\d+)$', crear_f2, name="crear_f2"),
    url(r'^crear_f3/(\d+)$', crear_f3, name="crear_f3"),
    url(r'^asistencia/(\d+)$', asistencia, name="asistencia"),
    url(r'^aceptar_formulario/(\d+)$', aceptar_formulario, name="aceptar_formulario"),
    url(r'^rechazar_formulario/(\d+)$', rechazar_formulario, name="rechazar_formulario"),
    url(r'^datos_alumnos/(\d+)$', datos_alumnos, name="datos_alumnos"),
    url(r'^datos_formulario/(\d+)$', datos_formulario, name="datos_formulario"),
    url(r'^volver/(\d+)$', volver, name="volver"),


    #URL de funciones sin ID.
    url(r'^traer_alumnos2/$', traer_alumnos2, name="traer_alumnos2"),
    url(r'^crearal/$', crear_alumno, name="crear_alumno"),
    url(r'^mod_alumno/$', mod_alumno, name="mod_alumno"),
    url(r'^crear_preceptor/$', crear_preceptor, name="crear_preceptor"),
    url(r'^busal/$', buscar_alumno, name="buscar_alumno"),
    url(r'^mis_alumnos/$', mis_alumnos, name="mis_alumnos"),

    #URL de cargra de Templates con filtros.
    url(r'^f2/$', f2, name="f2"),
    url(r'^formularios/$', formularios, name="formularios"),
    url(r'^traer_alumnos/$', traer_alumnos, name="traer_alumnos"),
    url(r'^mis_formularios/$', mis_formularios, name="mis_formularios"),
    url(r'^mis_alumnos_presentes/$', mis_alumnos_presentes, name="mis_alumnos_presentes")
]
