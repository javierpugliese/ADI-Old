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
from .models import *



#Función que crea F2 individuales
def crear_formulario2(request):
    if request.method == 'POST':
        #Tomamos los valores ingresados en el template
        nombre_alumno = request.POST['nombre']
        apellido_alumno = request.POST['apellido']
        dni_alumno = request.POST['dni']
        nombre_preceptor = request.POST['nombre_preceptor']
        ahorita = datetime.now()
        #Verificamos que los datos existan.
        preceptor = User.objects.get(username=nombre_preceptor)
        bpn = Alumno.objects.filter(nombre=nombre_alumno)
        bpa = Alumno.objects.filter(apellido=apellido_alumno)
        bpd = Alumno.objects.filter(dni=dni_alumno)
        if preceptor:
            if bpn:
                if bpa:
                    if bpd:
                        new_f2 = Formulario2(nombre_alumno=nombre_alumno, apellido_alumno=apellido_alumno, dni_alumno=dni_alumno, fecha=ahorita, preceptor=preceptor)
                        new_f2.save()
                        print "Creado"
                    else:
                        print "No existe un alumno con ese Dni"
                else:
                    print "No existe un alumno con ese apellido"
            else:
                print "No existe un alumno con ese nombre"
        else:
            print "NO SE CREA EL FORMULARIO, NO EXISTE EL PRECEPTOR"
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
        print year

        cur = Curso.objects.get(year=year, division=division)
        if cur:
            #Guardamos al alumnno
            al = Alumno(nombre=nombre, apellido=apellido, dni=dni, estado="Creado", curso=cur)
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

def alumnos(request):
   try:
       alumnos = Alumno.objects.filter(estado="Presente")
   except:
       alumnos = None
   return render(request,
                 'F2_grupal.html',
                 {'todos_los_alumnos':alumnos})

def retiro_grupal(request, alum_t):
    al = Alumno.objects.filter(dni=alum_t)
    if request.method == 'POST':
        al.update(estado="Retirado")
    return HttpResponse('FUNCIONO')

def volver(request, alum_t):
    al = Alumno.objects.filter(dni=alum_t)
    if request.method == 'POST':
        al.update(estado="Presente")
    return HttpResponse('FUNCIONO')


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
# Create your views here.
