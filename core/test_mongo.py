from pymongo import MongoClient
from django.conf import settings
from django.http import JsonResponse

def test_mongo(request):
    try:
        client = MongoClient(settings.MONGO_URI)
        client.admin.command('ping')
        return JsonResponse({"status": "Conectado a Mongo Atlas correctamente"})
    except Exception as e:
        return JsonResponse({"status": "Error", "detail": str(e)}, status=500)
