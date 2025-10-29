from flask import Blueprint

# Creamos el Blueprint para el módulo de encuestas
bp = Blueprint('surveys', __name__, template_folder='../templates/surveys') # Especificamos la carpeta de plantillas

# Importamos las rutas al final para evitar importaciones circulares
from app.surveys import routes
