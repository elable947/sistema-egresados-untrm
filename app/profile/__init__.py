# app/profile/__init__.py
from flask import Blueprint

# Creamos el Blueprint. 'profile' es el nombre que usaremos para url_for('profile.ruta')
bp = Blueprint('profile', __name__)

# Importamos las rutas DESPUÉS de definir bp
from app.profile import routes, forms

