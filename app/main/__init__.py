# app/main/__init__.py
from flask import Blueprint

bp = Blueprint('main', __name__)

# Importamos las rutas DESPUÉS de definir bp
from app.main import routes

