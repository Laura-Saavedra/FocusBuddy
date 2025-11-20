from django.urls import path
from core.views import test_mongo

from . import views

app_name = 'core'

urlpatterns = [

    path('', views.inicio, name='inicio'),

    path('tareas/', views.ListaTareasView.as_view(), name='lista_tareas'),
    path('tareas/nueva/', views.crear_tarea, name='crear_tarea'),
    path('tareas/<int:tarea_id>/', views.DetalleTareaView.as_view(), name='detalle_tarea'),
    path('tareas/<int:tarea_id>/editar/', views.editar_tarea, name='editar_tarea'),
    path('tareas/<int:tarea_id>/eliminar/', views.EliminarTareaView.as_view(), name='eliminar_tarea'),
    path('sesiones/', views.ListaSesionesView.as_view(), name='lista_sesiones'),
    path('sesiones/nueva/', views.crear_sesion, name='crear_sesion'),
    path('sesiones/<int:sesion_id>/',   views.DetalleSesionView.as_view(), name='detalle_sesion'),
    path('sesiones/<int:sesion_id>/editar/', views.editar_sesion, name='editar_sesion'),
    path('sesiones/<int:sesion_id>/eliminar/',  views.EliminarSesionView.as_view(), name='eliminar_sesion'),
    path('microlecciones/', views.microlecciones_index, name='microlecciones_index'),
    path('microlecciones/<int:id>/', views.microleccion_detalle, name='microleccion_detalle'),
    path('microlecciones/crear/', views.microleccion_crear, name='microleccion_crear'),
    path('test-mongo/', test_mongo),
]
