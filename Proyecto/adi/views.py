# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import *

#Función que crea F2
def crear_fm(request, dni_alumno):
    return HttpResponse("Funca")

def crear_f1(request, dni_alumno):
    return HttpResponse("Funca")

def crear_f2(request, dni_alumno):
    #Tomamos al usuario loggueado
    pepe = request.user
    #Buscamos al alumno a partir del Dni
    alumno2 = Alumno.objects.get(dni=dni_alumno)
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    if alumno2.estado=="Saliendo":
        return render(request, 'preceptor/usuario_con_form.html')
    else:
        #Modificamos el estado del alumno, para que este no aparezaca en usuarios disponibles para Formulario
        alumno2.estado="Saliendo"
        alumno2.save()
        ahorita = timezone.now()
        #Creamos el Formulario de tipo True ya que es un F2
        new_f = Formulario(alumno=alumno2, fecha=ahorita, estado="Proceso", preceptor=prec, tipo="True")
        new_f.save()
    return HttpResponse("Hecho")

def crear_f3(request, dni_alumno):
    #Tomamos al usuario loggueado
    pepe = request.user
    #Buscamos al alumno a partir del Dni
    alumno2 = Alumno.objects.get(dni=dni_alumno)
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    if alumno2.estado=="Saliendo":
        return render(request, 'preceptor/usuario_con_form.html')
    else:
        #Modificamos el estado del alumno, para que este no aparezaca en usuarios disponibles para Formulario
        alumno2.estado="Saliendo"
        alumno2.save()
        ahorita = timezone.now()
        #Creamos el Formulario de tipo False ya que es un F3
        new_f = Formulario(alumno=alumno2, fecha=ahorita, estado="Proceso", preceptor=prec, tipo="False")
        new_f.save()
    return HttpResponse('FUNCIONO')

def buscar_alumno(request):
    if request.method == 'POST':
        print "hola"
    return HttpResponse('FUNCIONO')

def modificar_alumno(request):
    print "nada"
    return HttpResponse('FUNCIONO')

def crear_alumno(request):
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    dni = request.POST['dni']
    num_curso = request.POST['num_curso']
    #Buscamos el curso
    cur = Curso.objects.get(numero=num_curso)
    if cur:
        #Buscamos el curso del preceptor
        al = Alumno(nombre=nombre, apellido=apellido, dni=dni, estado="Indefinido", curso=cur, faltas=0)
        al.save()
    else:
        print "HOla"

    return HttpResponse('FUNCIONO')


def crear_preceptor(request):
    if request.method == 'POST':
        print "llega"
        nombre_usuario = request.POST['nombre_usuario']
        password = request.POST['password']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        dni = request.POST['dni']
        #Creamos al modelo Preceptor a partir de los datos ingresados, relacionando nombre_usuario con el User creado
        preceptor = Preceptor(nombre_usuario=nombre_usuario,nombre=nombre, apellido=apellido, dni=dni)
        preceptor.save()
        #Creamos al usuario
        user = User.objects.create_user(username=nombre_usuario, password=password)
        user.save()
    return render(request, 'index.html')

def aceptar_formulario(request, alum_t):
    formulario = Formulario.objects.get(id=alum_t)
    nom = formulario.alumno.nombre
    al = Alumno.objects.get(nombre=nom)
    if al:
        al.estado="Retirado"
        al.save()
        formulario.estado="Finalizado"
        formulario.save()
        data = {
            'estado': al.nombre + " aceptado"
        }
    else:
        data = {
            'estado':"La operación falló"
        }
    return JsonResponse(data, safe=False)

def rechazar_formulario(request, alum_t):
    formulario = Formulario.objects.get(id=alum_t)
    nom = formulario.alumno.nombre
    al = Alumno.objects.get(nombre=nom)
    if al:
        al.estado="Indefinido"
        al.save()
        formulario.estado="Rechazado"
        formulario.save()
        data = {
            'estado': al.nombre + " RECHAZADO"
        }
    else:
        data = {
            'estado':"La operación falló"
        }
    return JsonResponse(data, safe=False)

def presente(request, alum_id):
    al = Alumno.objectos.get(dni=alum_id)
    if request.method == 'POST':
        al.estado="Presente"
        al.save()
    return HttpResponse('FUNCIONO')

def volver(request, alum_t):
    al = Alumno.objects.filter(dni=alum_t)
    if request.method == 'POST':
        al.update(estado="Presente")
    return HttpResponse('FUNCIONO')

def datos_alumnos(request, id_for):
    al = Alumno.objects.get(dni=id_for)
    return render (request, 'preceptor/elegir_formulario.html', {'alumno':al})

def datos_formulario(request, id_for):
    print id_for;
    formi = Formulario.objects.get(id=id_for)
    alum = formi.alumno
    return render(request,
                  'guardia/datos.html',
                  {'form':formi})

""" Reloj
<html>
<head>
<script>
function startTime() {
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  m = checkTime(m);
  s = checkTime(s);
  document.getElementById('txt').innerHTML =
  h + ":" + m + ":" + s;
  var t = setTimeout(startTime, 500);
}
function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}
</script>
</head>

<body onload="startTime()">

<div id="txt"></div>

</body>
</html>
"""

# =========================================================================
# Funciones de carga de template

def preceptor(request):
    return render(request, 'preceptor/prueba.html')

def cpreceptor(request):
    return render(request, 'admin/crear_preceptor.html')

def index(request):
    return render(request, 'inicio.html')

def chalumno(request):
    return render(request, 'admin/modificar_alumno.html')

def calumno(request):
    return render(request, 'admin/cargar_alumno.html')

def guardia(request):
    return render(request, 'guardia.html')

def inicio(request):
  return render(request, 'index.html')

def login_p(request):
    return render(request, 'login.html')

def f2(request):
    pepe = request.user
    try:
        prec = Preceptor.objects.get(nombre_usuario=pepe)
        al = Alumno.objects.filter(curso=prec.curso, estado="Presente").order_by('-apellido')
    except:
        al = None
    return render(request,
                 'preceptor/elegir_formulario.html',
                 {'todos_los_alumnos':al})

def formularios(request):
    try:
        forms2 = Formulario.objects.filter(tipo="True", estado="Proceso")
        forms3 = Formulario.objects.filter(tipo="False", estado="Proceso")
    except:
        forms2 = None
        forms3 = None
    print forms2
    print forms3
    return render(request,'guardia/formularios.html',{'todos_los_f3':forms3, 'todos_los_f2':forms2})

def mis_alumnos_presentes(request):
    pepe = request.user
    prec = Preceptor.objects.filter(nombre_usuario=pepe)
    al = Alumno.objects.filter(curso__preceptor=prec, estado="Presente")
    return render(request,
                 'preceptor/mis_alumnos_presentes.html',
                 {'todos_los_alumnos':al})

def mis_alumnos(request):
    pepe = request.user
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    al = Alumno.objects.filter(curso__preceptor=prec)
    return render(request,
                 'preceptor/mis_alumnos_presentes.html',
                 {'todos_los_alumnos':al})

def mis_formularios(request):
    pepe = request.user
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    try:
        forms2 = Formulario.objects.filter(tipo="True", estado="Proceso", preceptor=prec)
        forms3 = Formulario.objects.filter(tipo="False", estado="Proceso", preceptor=prec)
    except:
        forms2 = None
        forms3 = None
    return render(request,'preceptor/mis_formularios.html',{'todos_los_f3':forms3, 'todos_los_f2':forms2})
