from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tarea, SesionEstudio, MicroLeccion
from .forms import MicroLeccionForm, TareaForm, SesionEstudioForm
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from pymongo import MongoClient
from django.conf import settings
from django.http import JsonResponse
import certifi

# --- Función para conectarse a Mongo Atlas ---
def get_mongo_db():
    try:
        client = MongoClient(
            settings.MONGO_URI,
            tls=True,
            tlsCAFile=certifi.where()
        )
        return client[settings.MONGO_DB_NAME]
    except Exception as e:
        print("Error conectando a Mongo Atlas:", e)
        return None

# --- Inicio ---
def inicio(request):
    lecciones = MicroLeccion.objects.all()[:5]
    tareas = Tarea.objects.all().order_by('-creada_en')[:5]
    return render(request, 'core/inicio.html', {'lecciones': lecciones, 'tareas': tareas})

# --- Lista de Tareas ---
class ListaTareasView(ListView):
    model = Tarea
    template_name = 'core/lista_tareas.html'
    context_object_name = 'tareas'
    def get_queryset(self):
        return Tarea.objects.all().order_by('-creada_en')

# --- Crear Tarea ---
def crear_tarea(request):
    if not request.user.is_authenticated:
        return redirect('core:lista_tareas')

    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user
            tarea.save()  # SQLite

            db = get_mongo_db()
            if db is not None:
                try:
                    db["tareas"].insert_one({
                        "_id_sqlite": tarea.id,
                        "usuario": request.user.username,
                        "titulo": tarea.titulo,
                        "descripcion": tarea.descripcion,
                        "minutos_estimados": tarea.minutos_estimados,
                        "completada": tarea.completada,
                        "creada_en": tarea.creada_en.isoformat(),
                    })
                except Exception as e:
                    print("Error guardando tarea en Mongo:", e)

            return redirect('core:lista_tareas')
    else:
        form = TareaForm()
    return render(request, 'core/crear_tarea.html', {'form': form})

# --- Detalle de Tarea ---
class DetalleTareaView(DetailView):
    model = Tarea
    template_name = 'core/detalle_tarea.html'
    pk_url_kwarg = 'tarea_id'

# --- Editar Tarea ---
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()  # SQLite
            db = get_mongo_db()
            if db is not None:
                try:
                    db["tareas"].update_one(
                        {"_id_sqlite": tarea.id},
                        {"$set": {
                            "titulo": tarea.titulo,
                            "descripcion": tarea.descripcion,
                            "minutos_estimados": tarea.minutos_estimados,
                            "completada": tarea.completada,
                        }}
                    )
                except Exception as e:
                    print("Error actualizando tarea en Mongo:", e)
            return redirect('core:detalle_tarea', tarea_id=tarea.id)
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'core/editar_tarea.html', {'form': form, 'tarea': tarea})

# --- Eliminar Tarea ---
class EliminarTareaView(DeleteView):
    model = Tarea
    template_name = 'core/eliminar_tarea.html'
    pk_url_kwarg = 'tarea_id'
    success_url = reverse_lazy('core:lista_tareas')

    def delete(self, request, *args, **kwargs):
        tarea = self.get_object()
        response = super().delete(request, *args, **kwargs)  # SQLite principal
        db = get_mongo_db()
        if db is not None:
            try:
                db["tareas"].delete_one({"_id_sqlite": tarea.id})
            except Exception as e:
                print("Error eliminando tarea en Mongo:", e)
        return response

# --- Sesiones ---
def crear_sesion(request):
    tareas_usuario = Tarea.objects.filter(completada=False).order_by('-creada_en')
    if request.method == 'POST':
        form = SesionEstudioForm(request.POST)
        form.fields['tarea'].queryset = tareas_usuario
        if form.is_valid():
            sesion = form.save(commit=False)
            sesion.usuario = None
            sesion.fin_en = timezone.now()
            sesion.save()
            return redirect('core:detalle_sesion', sesion_id=sesion.id)
    else:
        form = SesionEstudioForm()
        form.fields['tarea'].queryset = tareas_usuario
    return render(request, 'core/crear_sesion.html', {'form': form})

class DetalleSesionView(DetailView):
    model = SesionEstudio
    template_name = 'core/detalle_sesion.html'
    pk_url_kwarg = 'sesion_id'
    context_object_name = 'sesion'

class ListaSesionesView(ListView):
    model = SesionEstudio
    template_name = 'core/lista_sesiones.html'
    context_object_name = 'sesiones'
    def get_queryset(self):
        return SesionEstudio.objects.all().order_by('-inicio_en')

def editar_sesion(request, sesion_id):
    sesion = get_object_or_404(SesionEstudio, pk=sesion_id)
    if request.method == 'POST':
        form = SesionEstudioForm(request.POST, instance=sesion)
        if form.is_valid():
            form.save()
            return redirect('core:detalle_sesion', sesion_id=sesion.id)
    else:
        form = SesionEstudioForm(instance=sesion)
    return render(request, 'core/editar_sesion.html', {'form': form, 'sesion': sesion})

class EliminarSesionView(DeleteView):
    model = SesionEstudio
    template_name = 'core/eliminar_sesion.html'
    pk_url_kwarg = 'sesion_id'
    success_url = reverse_lazy('core:lista_sesiones')
    context_object_name = 'sesion'

# --- Microlecciones ---
def microlecciones_index(request):
    lecciones = MicroLeccion.objects.all()
    return render(request, "core/microlecciones_index.html", {"lecciones": lecciones})

def microleccion_detalle(request, id):
    leccion = get_object_or_404(MicroLeccion, id=id)
    return render(request, "core/microleccion_detalle.html", {"leccion": leccion})

def microleccion_crear(request):
    if request.method == 'POST':
        form = MicroLeccionForm(request.POST)
        if form.is_valid():
            leccion = form.save()  # SQLite
            db = get_mongo_db()
            if db is not None:
                try:
                    db["microlecciones"].insert_one({
                        "_id_sqlite": leccion.id,
                        "titulo": leccion.titulo,
                        "contenido": leccion.contenido,
                        "duracion_estimada": leccion.duracion_estimada,
                        "creada_en": leccion.creada_en.isoformat(),
                    })
                except Exception as e:
                    print("Error guardando microlección en Mongo:", e)
            return redirect('core:microlecciones_index')
    else:
        form = MicroLeccionForm()
    return render(request, 'core/microleccion_crear.html', {'form': form})

# --- Test Mongo ---
def test_mongo(request):
    db = get_mongo_db()
    if db is not None:
        try:
            tareas = db["tareas"]
            result = tareas.insert_one({"titulo": "Prueba desde test-mongo"})
            return JsonResponse({"inserted": str(result.inserted_id)})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Mongo Atlas no disponible"}, status=500)
