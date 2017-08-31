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
def mostrar_opciones(request, alum_t):
    al = Alumno.objects.get(dni=alum_t)
    return render(request,
                  'preceptor/elegir_form.html',
                  {'alumno':al})

def crear_fm(request, dni_alumno):
    return HttpResponse("Funca")

def crear_f1(request, dni_alumno):
    return HttpResponse("Funca")

def crear_f2(request, dni_alumno):
    pepe = request.user
    ahorita = timezone.now()
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    alumno = Alumno.objects.get(curso=prec.curso, dni=dni_alumno)
    if alumno.estado=="Saliendo":
        return render(request, 'preceptor/usuario_con_form.html')
    else:
        alumno.estado="Saliendo"
        alumno.save()
        new_f2 = Formulario2(alumno=alumno, fecha=ahorita, estado="Proceso", preceptor=prec)
        new_f2.save()
        try:
            f2s = Formulario2.objects.filter(preceptor=prec, estado="Proceso")
        except:
            f2s = None
        return render(request,
                      'preceptor/confirmar_F2.html',
                      {'f2':f2s})

def confirmar_f2(request):
    pepe = request.user
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    del_f2 = Formulario2.objects.filter(estado="Proceso", preceptor=prec)
    for a in del_f2:
        a.estado="Verificar"
        a.save()
    return HttpResponse('HECHO')

def confirmar_f3(request):
    pepe = request.user
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    del_f3 = Formulario3.objects.filter(estado="Proceso")
    for a in del_f3:
        a.estado="Verificar"
        a.save()
    return HttpResponse('HECHO')


def crear_f3(request):
    pepe = request.user
    ahorita = timezone.now()
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    alumno = Alumno.objects.filter(curso=prec.curso, dni=dni_alumno)
    alumno.estado="Indefinido"
    new_f3 = Formulario3(alumno=a, fecha=ahorita, estado="Proceso", preceptor=prec)
    new_f3.save()
    try:
        f3s = Formulario3.objects.filter(preceptor=prec, estado="Proceso")
    except:
        f3s = None
    return render(request,
                  'preceptor/confirmar_F3.html',
                  {'f3s':f3})

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
                 'preceptor/elegir_formulario.html',
                 {'todos_los_alumnos':al})

def formularios(request):
    try:
        forms2 = Formulario2.objects.filter(estado="Verificar")
        forms3 = Formulario3.objects.filter(estado="Verificar")
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

def mis_formularios(request):
    pepe = request.user
    prec = Preceptor.objects.get(nombre_usuario=pepe)
    try:
        forms2 = Formulario2.objects.filter(estado="Proceso", preceptor=prec)
        forms3 = Formulario3.objects.filter(estado="Proceso", preceptor=prec)
    except:
        forms2 = None
        forms3 = None
    return render(request,'preceptor/mis_formularios.html',{'todos_los_f3':forms3, 'todos_los_f2':forms2})
