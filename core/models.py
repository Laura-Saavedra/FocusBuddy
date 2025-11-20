from django.db import models
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Tarea(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='tareas',
        null=True,       
        blank=True       
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    minutos_estimados = models.PositiveIntegerField(default=25)
    completada = models.BooleanField(default=False)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class SesionEstudio(models.Model):
    POMODORO = 'Pomodoro'
    PERSONALIZADA = 'Personalizada'
    TIPOS_SESION = [
        (POMODORO, 'Pomodoro'),
        (PERSONALIZADA, 'Personalizada')
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='sesiones',
        null=True,      
        blank=True       
    )
    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.SET_NULL,
        related_name='sesiones',
        null=True,
        blank=True
    )
    tipo_sesion = models.CharField(
        max_length=20,
        choices=TIPOS_SESION,
        default=POMODORO
    )
    duracion_minutos = models.PositiveIntegerField()
    inicio_en = models.DateTimeField()
    fin_en = models.DateTimeField(null=True, blank=True)
    notas = models.TextField(blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username if self.usuario else 'Sin usuario'} - {self.tipo_sesion} @ {self.inicio_en}"


class MicroLeccion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    duracion_estimada = models.PositiveIntegerField(default=5)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
