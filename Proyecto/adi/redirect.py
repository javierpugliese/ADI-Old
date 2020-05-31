#from django.shortcuts import render_to_response, render, redirect
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import *

def preceptor(request):
    return render(request, 'preceptor/index.html')

def cpreceptor(request):
    return render(request, 'admin/crear_preceptor.html')

def index(request):
    return render (request, "inicio.html")
    #return render (request, "preceptor/charts.html")

def index_guardia(request):
    pepe = request.user
    if pepe.email.endswith('@preceptor.com'):
        return render(request, 'rechazado.html')
    return render(request, 'guardia/index.html')

def chalumno(request):
    return render(request, 'admin/modificar_alumno.html')

def calumno(request):
    return render(request, 'admin/cargar_alumno.html')

def guardia(request):
    return render(request, 'guardia.html')

def inicio(request):
  return render(request, 'index.html')

def ver_charts(request):
    return render(request, 'preceptor/charts.html')

def login_p(request):
    return render(request, 'login.html')
