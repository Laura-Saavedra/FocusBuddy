from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tarea

User = get_user_model()

class TareaTestCase(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="testuser", password="12345")
        self.tarea1 = Tarea.objects.create(titulo="Tarea 1", completada=False, usuario=self.usuario)
        self.tarea2 = Tarea.objects.create(titulo="Tarea 2", completada=True, usuario=self.usuario)

    def test_tarea_creacion(self):
        self.assertEqual(self.tarea1.titulo, "Tarea 1")
        self.assertFalse(self.tarea1.completada)
        self.assertEqual(self.tarea1.usuario.username, "testuser")

    def test_tareas_completadas(self):
        completadas = Tarea.objects.filter(completada=True, usuario=self.usuario)
        self.assertEqual(completadas.count(), 1)
        self.assertEqual(completadas.first().titulo, "Tarea 2")

    def test_tareas_pendientes(self):
        pendientes = Tarea.objects.filter(completada=False, usuario=self.usuario)
        self.assertEqual(pendientes.count(), 1)
        self.assertEqual(pendientes.first().titulo, "Tarea 1")
