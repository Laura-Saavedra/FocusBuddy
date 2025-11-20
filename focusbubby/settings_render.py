# settings_render.py
import os
from .settings import BASE_DIR

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = ['focusbuddy-e9mo.onrender.com']

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"
