# -*- coding: utf-8 -*-
"""
Punto de entrada para ejecutar la aplicación.
Este archivo importa la "factory" (create_app) y le pasa
la configuración.
"""

# Importamos la factory de nuestra carpeta 'app'
from app import create_app
# Importamos la clase Config desde el archivo 'config.py'
from config import Config

# Creamos la instancia de la app pasándole la clase de configuración
app = create_app(Config)

# Esto permite ejecutar la app con "python run.py"
if __name__ == '__main__':
    app.run()

