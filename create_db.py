# -*- coding: utf-8 -*-
"""
Script manual para crear la base de datos (Plan B).
Ejecutar esto si 'flask db upgrade' falla.
"""

import os
from app import create_app, db
from config import Config

# Creamos una instancia de la app usando la "factory" y la configuración
app = create_app(Config)

# Definimos la ruta absoluta para el archivo de la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'app.db')

def create_database():
    print("Iniciando la creación de la base de datos...")
    
    # Usamos un "app context" para que SQLAlchemy sepa a qué app pertenece
    with app.app_context():
        
        # --- ¡ESTA ES LA LÍNEA QUE FALTABA! ---
        # Importamos los modelos para que SQLAlchemy los "conozca"
        # antes de llamar a create_all()
        from app import models 
        # --------------------------------------

        # Verificamos si el archivo app.db ya existe
        if os.path.exists(db_path):
            print(f"El archivo '{db_path}' ya existe.")
            print("Si quieres recrearlo, bórralo manualmente y ejecuta este script de nuevo.")
        else:
            # Esta es la línea mágica que lee models.py y crea todas las tablas
            db.create_all()
            print("--------------------------------------------------")
            print(f"¡Éxito! El archivo 'app.db' ha sido creado en:")
            print(f"{db_path}")
            print("--------------------------------------------------")

if __name__ == '__main__':
    create_database()

