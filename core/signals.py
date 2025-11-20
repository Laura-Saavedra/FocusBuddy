from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict

from .models import Tarea, SesionEstudio, MicroLeccion
from .mongo import tareas_col, sesiones_col, microlecciones_col


# ----------- TAREAS -----------
@receiver(post_save, sender=Tarea)
def sync_tarea(sender, instance, created, **kwargs):
    data = model_to_dict(instance)
    data["_id"] = instance.id  # Usamos el ID de Django como ID en Mongo

    tareas_col.update_one(
        {"_id": instance.id},
        {"$set": data},
        upsert=True
    )


@receiver(post_delete, sender=Tarea)
def delete_tarea(sender, instance, **kwargs):
    tareas_col.delete_one({"_id": instance.id})


# ----------- SESIONES -----------
@receiver(post_save, sender=SesionEstudio)
def sync_sesion(sender, instance, created, **kwargs):
    data = model_to_dict(instance)
    data["_id"] = instance.id

    sesiones_col.update_one(
        {"_id": instance.id},
        {"$set": data},
        upsert=True
    )


@receiver(post_delete, sender=SesionEstudio)
def delete_sesion(sender, instance, **kwargs):
    sesiones_col.delete_one({"_id": instance.id})


# ----------- MICROLECCIONES -----------
@receiver(post_save, sender=MicroLeccion)
def sync_microleccion(sender, instance, created, **kwargs):
    data = model_to_dict(instance)
    data["_id"] = instance.id

    microlecciones_col.update_one(
        {"_id": instance.id},
        {"$set": data},
        upsert=True
    )


@receiver(post_delete, sender=MicroLeccion)
def delete_microleccion(sender, instance, **kwargs):
    microlecciones_col.delete_one({"_id": instance.id})
