from flask import Blueprint

# Creamos el Blueprint para los ajustes generales del usuario
bp = Blueprint('user_settings', __name__, template_folder='../templates/user_settings')

# Importamos las rutas al final para evitar importaciones circulares
from app.user_settings import routes

