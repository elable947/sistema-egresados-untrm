# app/auth/__init__.py
from flask import Blueprint

# Creamos el Blueprint. 'auth' es el nombre que usaremos para url_for('auth.ruta')
bp = Blueprint('auth', __name__)

# Importamos las rutas DESPUÉS de definir bp para evitar ciclos
from app.auth import routes, forms 

