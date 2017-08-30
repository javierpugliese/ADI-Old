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



#Función que crea F2 individuales
def mostrar_opciones(request, alum_t):
    al = Alumno.objects.get(dni=alum_t)
    return render(request,
                  'preceptor/F2_grupal.html',
                  {'alumno':al})

def crear_f2(request, nada):
    print nada
    pepe = request.user
    ahorita = timezone.now()
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    todos = Alumno.objects.filter(curso=prec.curso, estado="Indefinido")
    if todos:
        for a in todos:
            print "encuentra"
            a.estado="Saliendo"
            a.save()
            print a.estado
            new_f2 = Formulario2(alumno=a, fecha=ahorita, estado="Proceso", preceptor=prec)
            new_f2.save()
    else:
        print "No encuentra"
    data = {
        'estado': "activo"
    }
    return JsonResponse(data, safe=False)

def crear_f3(request):
    print "nada"

def buscar_alumno(request):
    if request.method == 'POST':
        print "hola"
    return HttpResponse('FUNCIONO')

def modificar_alumno(request):
    print "nada"


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
        nombre_usuario = request.POST['nombre_usuario']
        password = request.POST['password']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        dni = request.POST['dni']
        year = request.POST['year']
        division = request.POST['division']
        cur = Curso.objects.get(year=year, division=division)
        #Creamos al modelo Preceptor a partir de los datos ingresados, relacionando nombre_usuario con el User creado
        preceptor = Preceptor(nombre_usuario=nombre_usuario,nombre=nombre, apellido=apellido, dni=dni, curso=cur)
        preceptor.save()
        #Creamos al usuario
        user = User.objects.create_user(username=nombre_usuario, password=password)
        user.save()
    return render(request, 'index.html')

def retiro_grupal(request, alum_t):
    al = Alumno.objects.filter(dni=alum_t)
    if request.method == 'POST':
        al.update(estado="Retirado")
    return HttpResponse('FUNCIONO')

def aceptar_f2(request, alum_t):
    f2 = Formulario2.objects.get(id=alum_t)
    nom = f2.alumno.nombre
    al = Alumno.objects.get(nombre=nom)
    if al:
        al.estado="Retirado"
        al.save()
        f2.estado="Finalizado"
        f2.save()
        data = {
            'estado':"Operación realizada con éxito"
        }
    else:
        data = {
            'estado':"La operación falló"
        }
    return JsonResponse(data, safe=False)

def aceptar_f3(request, alum_t):
    f3 = Formulario3.objects.get(id=alum_t)
    nom = f3.alumno.nombre
    al = Alumno.objects.get(nombre=nom)
    if al:
        al.estado="Retirado"
        al.save()
        f3.estado="Finalizado"
        f3.save()
        data = {
            'estado':"Operación realizada con éxito"
        }
    else:
        data = {
            'estado':"La operación falló"
        }
    return JsonResponse(data, safe=False)

def rechazar_f2(request, alum_t):
    f2 = Formulario2.objects.get(id=alum_t)
    nom = f2.alumno.nombre
    al = Alumno.objects.get(nombre=nom)
    if al:
        al.estado="Indefinido"
        al.save()
        f2.estado="Rechazado"
        f2.save()
        data = {
            'estado':"Operación realizada con éxito"
        }
    else:
        data = {
            'estado':"La operación falló"
        }
    return JsonResponse(data, safe=False)

def rechazar_f3(request, alum_t):
    f3 = Formulario3.objects.get(id=alum_t)
    nom = f3.alumno.nombre
    al = Alumno.objects.get(nombre=nom)
    if al:
        al.estado="Indefinido"
        al.save()
        f3.estado="Rechazado"
        f3.save()
        data = {
            'estado':"Operación realizada con éxito"
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
    print id_for;
    al = Alumno.objects.get(dni=id_for)
    return JsonResponse(data, safe=False)

def datos_f2(request, id_for):
    print id_for;
    formi = Formulario2.objects.get(id=id_for)
    alum = formi.alumno
    return render(request,
                  'guardia/datos.html',
                  {'form':formi})
    #return JsonResponse(data, safe=False)

def datos_f3(request, id_for):
    print id_for;
    formi = Formulario3.objects.get(id=id_for)
    data = {
        'preceptor':formi.preceptor.username,
        'alumno':formi.alumno.nombre,
        'fecha':formi.fecha,
        'estado':formi.estado
    }
    return JsonResponse(data, safe=False)

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

def chalumno(request):
    return render(request, 'admin/modificar_alumno.html')

def calumno(request):
    return render(request, 'admin/cargar_alumno.html')

def guardia(request):
    return render(request, 'guardia.html')

def inicio(request):
  return render(request, 'index.html')

def alumnos_para_formulario(request):
    pepe = request.user
    try:
        prec = Preceptor.objects.get(nombre_usuario=pepe)
        al = Alumno.objects.filter(curso=prec.curso, estado="Presente").order_by('-apellido')
    except:
        al = None
    return render(request,
                 'preceptor/F2.html',
                 {'todos_los_alumnos':al})

def f2(request):
    pepe = request.user
    try:
        prec = Preceptor.objects.get(nombre_usuario=pepe)
        al = Alumno.objects.filter(curso=prec.curso, estado="Presente").order_by('-apellido')
    except:
        al = None
    return render(request,
                 'preceptor/F2.html',
                 {'todos_los_alumnos':al})

def f3(request):
    return render(request, 'preceptor/F3.html')

def f2grupal(request):
   try:
       alumnos = Alumno.objects.filter(estado="Presente")
   except:
       alumnos = None
   return render(request,
                 'preceptor/F2_grupal.html',
                 {'todos_los_alumnos':alumnos})

def aux_f2(request):
   try:
       alumnos = Alumno.objects.filter(estado="Presente")
   except:
       alumnos = None
   return render(request,
                 'preceptor/aux_f2.html',
                 {'todos_los_alumnos':alumnos})

def formularios(request):
    try:
        forms2 = Formulario2.objects.filter(estado="Proceso")
        forms3 = Formulario3.objects.filter(estado="Proceso")
    except:
        forms2 = None
        forms3 = None
    return render(request,'guardia/formularios.html',{'todos_los_f3':forms3, 'todos_los_f2':forms2})

def mis_alumnos(request):
    pepe = request.user
    try:
        prec = Preceptor.objects.get(nombre_usuario=pepe)
        al = Alumno.objects.filter(curso=prec.curso).order_by('-apellido')
    except:
        al = None
    return render(request,
                 'preceptor/mis_alumnos.html',
                 {'todos_los_alumnos':al})
