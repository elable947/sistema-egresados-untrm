import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Inicialización global
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Por favor, inicie sesión para acceder a esta página.'
login.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # --- Registrar Blueprints ---
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    #from app.networking import bp as networking_bp
    #app.register_blueprint(networking_bp) # Aunque no tenga rutas, lo registramos

    from app.surveys import bp as surveys_bp
    app.register_blueprint(surveys_bp)

    # --- REGISTRAMOS EL NUEVO BLUEPRINT: user_settings ---
    from app.user_settings import bp as user_settings_bp
    app.register_blueprint(user_settings_bp) # Sin prefijo, rutas como /mi-perfil

    # Importación de modelos DENTRO de la factory y contexto
    with app.app_context():
        from app import models

    return app

