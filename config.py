import os

# --- Ruta Base del Proyecto ---
# Obtiene la ruta absoluta de la carpeta donde está este archivo (config.py)
# Asumiendo que config.py está en la raíz del proyecto (sistema_egresados)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # --- Clave Secreta ---
    # ¡MUY IMPORTANTE! Cambia esto por una cadena aleatoria y segura en producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-dificil-de-adivinar'

    # --- Configuración de la Base de Datos ---
    # Usaremos SQLite para desarrollo local (un archivo simple)
    # Apunta a sistema_egresados/app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Opción para desactivar el seguimiento de modificaciones (ahorra recursos)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Configuración para Subida de Archivos (Fotos de Perfil) ---
    # Ruta base de la carpeta 'static' dentro de 'app'
    static_folder_abs = os.path.join(basedir, 'app', 'static')

    # Ruta relativa DENTRO de 'static' donde se guardarán las subidas
    UPLOAD_FOLDER_REL = 'uploads'
    PROFILE_PICS_FOLDER_REL = os.path.join(UPLOAD_FOLDER_REL, 'profile_pics') # Será 'uploads/profile_pics'

    # Rutas ABSOLUTAS donde se guardarán físicamente los archivos
    # Usadas por Python para guardar el archivo: sistema_egresados/app/static/uploads/profile_pics/
    UPLOAD_FOLDER_ABS = os.path.join(static_folder_abs, UPLOAD_FOLDER_REL)
    PROFILE_PICS_FOLDER_ABS = os.path.join(static_folder_abs, PROFILE_PICS_FOLDER_REL)

    # Asegurarse de que las carpetas existan al iniciar la app
    os.makedirs(UPLOAD_FOLDER_ABS, exist_ok=True)
    os.makedirs(PROFILE_PICS_FOLDER_ABS, exist_ok=True)

    # Límite de tamaño máximo del archivo subido (ej. 1MB)
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024 # 1 Megabyte

    # Extensiones permitidas (para seguridad)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # --- Otras Configuraciones (Opcionales pero recomendadas) ---
    # Configuración para Flask-Login (si necesitas personalizar, ej. nombre de cookie)
    # REMEMBER_COOKIE_DURATION = timedelta(days=7)
    # REMEMBER_COOKIE_SECURE = True # Solo HTTPS en producción
    # REMEMBER_COOKIE_HTTPONLY = True

    # Configuración de email (si añades recuperación de contraseña)
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['tu_email@ejemplo.com']

