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
def crear_formulario2(request):
    if request.method == 'POST':
        #Tomamos los valores ingresados en el template
        nombre_alumno = request.POST['nombre']
        apellido_alumno = request.POST['apellido']
        dni_alumno = request.POST['dni']
        nombre_usuario = request.POST['nombre_preceptor']
        ahorita = datetime.now()
        prec = User.objects.get(username=nombre_usuario)
        #Verificamos que los datos existan.
        al = Alumno.objects.get(nombre=nombre_alumno, apellido=apellido_alumno, dni=dni_alumno)
        if prec and al:
            new_f2 = Formulario2(alumno=al, preceptor=prec, fecha=ahorita, estado="Proceso")
            new_f2.save()
        else:
            print "NONONO"
        return redirect ('cambio')
    return HttpResponse('HOLA <b style="color: red">SOLO PODES ACCEDER POR POST</b>')

def crear_formulario3(request):
    if request.method == 'POST':
        #Igual que el F2 individual
        nombre_alumno = request.POST['nombre2']
        apellido_alumno = request.POST['apellido2']
        dni_alumno = request.POST['dni2']
        nombre_usuario = request.POST['preceptor2']
        ahorita = datetime.now()
        prec = User.objects.get(username=nombre_usuario)
        al = Alumno.objects.get(nombre=nombre_alumno, apellido=apellido_alumno, dni=dni_alumno)
        if prec and al:
            new_f3 = Formulario3(alumno=al, preceptor=prec, fecha=ahorita)
            new_f3.save()
        else:
            print "NONONO"
        return redirect ('cambio')
    return HttpResponse('HOLA <b style="color: red">SOLO PODES ACCEDER POR POST</b>')

def buscar_alumno(request):
    if request.method == 'POST':
        #Tomamos los valores ingresados en el template
        nombre = request.POST['nombre3']
        apellido = request.POST['apellido3']
        dni = request.POST['dni3']
        #Corroboramos que los datos ingresados sean de un alumno
        global aux
        aux = Alumno.objects.filter(nombre=nombre, apellido=apellido,dni=dni)
        if aux:
            print "Existe"
        else:
            print "NO EXISTE"
    return HttpResponse('FUNCIONO')

def modificar_alumno(request):
    print "Arrancamos"
    if request.method == 'POST':
        n_nombre = request.POST['nombre4']
        n_apellido = request.POST['apellido4']
        n_dni = request.POST['dni4']
        aux.update(nombre=n_nombre, apellido=n_apellido, dni=n_dni)
    return HttpResponse('FUNCIONO')


def crear_alumno(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        dni = request.POST['dni']
        year = request.POST['year']
        division = request.POST['division']
        #Buscamos el curso indicado para hacer la FK.
        cur = Curso.objects.get(year=year, division=division)
        if cur:
            #Guardamos al alumnno
            al = Alumno(nombre=nombre, apellido=apellido, dni=dni, estado="Indefinido", curso=cur, faltas=0)
            al.save()
        else:
            print "No existe ese curso"
    return render(request, 'index.html')


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

def aceptar(request, alum_t):
    f2 = Formulario2.objects.get(id=alum_t)
    if request.method == 'POST':
        nom = f2.alumno.nombre
        al = Alumno.objects.get(nombre=nom)
        if al:
            al.estado="Retirado"
            al.save()
            f2.estado="Usado"
            f2.save()
        else:
            print "No hay"
    return HttpResponse('FUNCIONO')

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

def pepe(request, id_for):
    print id_for;
    al = Alumno.objects.get(dni=id_for)
    data = {
        'apellido':al.apellido,
        'nombre':al.nombre,
        'dni':al.dni,
        'estado':al.estado
    }
    return JsonResponse(data, safe=False)

def datos_f2(request, id_for):
    print id_for;
    formi = Formulario2.objects.get(id=id_for)
    data = {
        'preceptor':formi.preceptor.username,
        'alumno':formi.alumno.nombre,
        'fecha':formi.fecha,
        'estado':formi.estado
    }
    return JsonResponse(data, safe=False)

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
    return render(request, 'preceptor.html')

def cpreceptor(request):
    return render(request, 'crear_preceptor.html')

def chalumno(request):
    return render(request, 'modificar_alumno.html')

def calumno(request):
    return render(request, 'crear_alumno.html')

def guardia(request):
    return render(request, 'guardia.html')

def alumno(request):
    return render(request, 'alumno.html')

def picker(request):
    return render(request, 'picker.html')

def inicio(request):
  return render(request, 'index.html')

def f2(request):
    return render(request, "F2.html")

def alumnos(request):
   try:
       alumnos = Alumno.objects.filter(estado="Presente")
   except:
       alumnos = None
   return render(request,
                 'F2_grupal.html',
                 {'todos_los_alumnos':alumnos})

def formularios(request):
    try:
        forms2 = Formulario2.objects.all()
        forms3 = Formulario3.objects.all()
    except:
        forms2 = None
        forms3 = None
    return render(request,'formularios.html',{'todos_los_f3':forms3, 'todos_los_f2':forms2})

def mis_alumnos(request):
    pepe = request.user
    try:
        prec = Preceptor.objects.get(nombre_usuario=pepe)
        al = Alumno.objects.filter(curso=prec.curso).order_by('-apellido')
    except:
        al = None
    return render(request,
                 'mis_alumnos.html',
                 {'todos_los_alumnos':al})

def f2s(request):
   try:
       f2 = Formulario2.objects.filter(estado="Presente")
   except:
       f2 = None
   return render(request,
                 'guardia.html',
                 {'todos_los_f2':f2})
