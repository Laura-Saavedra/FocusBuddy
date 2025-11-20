from django.contrib import admin
from .models import Tarea, SesionEstudio, MicroLeccion


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'completada', 'creada_en')


@admin.register(SesionEstudio)
class SesionEstudioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_sesion', 'inicio_en', 'fin_en')


@admin.register(MicroLeccion)
class MicroLeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'duracion_estimada')

