from pymongo import MongoClient
from django.conf import settings
from django.http import JsonResponse
import certifi

def test_mongo(request):
    try:
        client = MongoClient(settings.MONGO_URI, tlsCAFile=certifi.where())
        client.admin.command('ping')  # prueba de conexión real
        return JsonResponse({"status": "Conectado a Mongo Atlas correctamente"})
    except Exception as e:
        return JsonResponse({"status": "Error", "detail": str(e)}, status=500)
