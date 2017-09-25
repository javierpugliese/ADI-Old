from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone

from django.db import models

class Guardia(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    dni = models.IntegerField(null=False)

    def __str__(self):
        return '{} {} '.format(self.apellido, self.nombre)

class Padre_Tutor(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    dni = models.IntegerField(null=False)
    email = models.EmailField(max_length=40)
    telefono = models.IntegerField()

    def __str__(self):
        return '{} '.format(self.nombre)

class Preceptor(models.Model):
    nombre_usuario = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    dni = models.IntegerField(null=False, primary_key=True)
    def __str__(self):
        return '{} '.format(self.nombre_usuario)

class Curso(models.Model):
    year = models.PositiveSmallIntegerField(default=1)
    division = models.CharField(max_length=1)
    numero = models.IntegerField(primary_key=True)
    preceptor = models.ForeignKey(Preceptor)
    def __str__(self):
        return ' {} - {} / {}'.format(self.year, self.division, self.numero)

class Alumno(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    dni = models.IntegerField(null=False)
    padre = models.ForeignKey(Padre_Tutor)
    curso = models.ForeignKey(Curso)
    faltas = models.FloatField(null=False)
    estado = models.CharField(max_length=14)

    def __str__(self):
        return '{} '.format(self.nombre)


#    def count_like(self):
#        return Like.objects.filter(tweet=self).count()

class Formulario(models.Model):
    preceptor = models.ForeignKey(Preceptor)
    alumno = models.ForeignKey(Alumno)
    fecha = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=11)
    # El estado de tipo determina el tipo de Formulario, True = F2, False = F3
    tipo = models.BooleanField()

    def __str__(self):
        return 'Formulario de {}'.format(self.alumno.nombre)

    def count_formularios(self):
        return Formulario.objects.filter(tweet=self).count()
