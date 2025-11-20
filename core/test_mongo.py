from pymongo import MongoClient
from django.conf import settings
from django.http import JsonResponse

def test_mongo(request):
    client = MongoClient(settings.MONGO_URI)
    db = client["focusbuddy"]
    tareas = db["tareas"]

    # prueba: insertar algo
    result = tareas.insert_one({"titulo": "Prueba", "completada": False})

    return JsonResponse({"inserted_id": str(result.inserted_id)})
