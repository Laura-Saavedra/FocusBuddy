from pymongo import MongoClient
from django.conf import settings
import certifi

# Conexión a Mongo Atlas usando certificados válidos
client = MongoClient(settings.MONGO_URI, tlsCAFile=certifi.where())
db = client[settings.MONGO_DB_NAME]  # usa el nombre de la DB real

# Colecciones
tareas_col = db["tareas"]
sesiones_col = db["sesiones"]
microlecciones_col = db["microlecciones"]
