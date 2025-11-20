from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client["focusbuddy"]

tareas_col = db["tareas"]
sesiones_col = db["sesiones"]
microlecciones_col = db["microlecciones"]
