# -*- coding: utf-8 -*-
"""
Definición de todos los modelos de la base de datos.
[...] Añadida tabla EncuestaAsignada y relaciones.
"""
from app import db, login
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import os
# --- (Otras clases de Modelo sin cambios: EgresadoPosgrado, Facultad, Carrera) ---
# --- Tablas de Asociación (Muchos a Muchos) ---
class EgresadoPosgrado(db.Model):
    # ... (sin cambios) ...
    __tablename__ = 'egresado_posgrado'

    id = db.Column(db.Integer, primary_key=True)
    egresado_id = db.Column(db.Integer, db.ForeignKey('egresado.id'))
    posgrado_id = db.Column(db.Integer, db.ForeignKey('posgrado.id'))
    fecha_vinculacion = db.Column(db.Date)
    observaciones = db.Column(db.Text)
    egresado = db.relationship('Egresado', back_populates='posgrados_asociados')
    posgrado = db.relationship('Posgrado', back_populates='egresados_asociados')

# --- Tablas de Estructura Académica (del PDF) ---
class Facultad(db.Model):
    # ... (sin cambios) ...
    __tablename__ = 'facultad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    siglas = db.Column(db.String(20), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    carreras = db.relationship('Carrera', back_populates='facultad', lazy='dynamic')
    autoridades = db.relationship('AutoridadUniversitaria', back_populates='facultad', lazy='dynamic')

    def __repr__(self):
        return f'<Facultad {self.nombre}>'

class Carrera(db.Model):
    # ... (sin cambios) ...
    __tablename__ = 'carrera'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    codigo = db.Column(db.String(50), nullable=True)
    duracion_anios = db.Column(db.Integer, nullable=True)
    id_facultad = db.Column(db.Integer, db.ForeignKey('facultad.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    facultad = db.relationship('Facultad', back_populates='carreras')
    egresados = db.relationship('Egresado', back_populates='carrera', lazy='dynamic')

    def __repr__(self):
        return f'<Carrera {self.nombre}>'

# --- Tablas de Perfiles de Usuario (Roles) ---
class Egresado(db.Model):
    __tablename__ = 'egresado'
    id = db.Column(db.Integer, primary_key=True)
    nombre1 = db.Column(db.String(100), nullable=False)
    nombre2 = db.Column(db.String(100), nullable=True)
    nombre3 = db.Column(db.String(100), nullable=True)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=True)
    dni = db.Column(db.String(15), unique=True, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    fecha_egreso = db.Column(db.Date, nullable=True)
    id_carrera = db.Column(db.Integer, db.ForeignKey('carrera.id'), nullable=False)
    pais_residencia = db.Column(db.String(100), nullable=True)
    ciudad_residencia = db.Column(db.String(100), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    foto_perfil_filename = db.Column(db.String(100), nullable=True, default='default.png')
    perfil_publico = db.Column(db.Boolean, default=False, nullable=False)
    mostrar_email_publico = db.Column(db.Boolean, default=False, nullable=False)
    fecha_registro = db.Column(db.DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    user_login = db.relationship('User', back_populates='perfil_egresado', uselist=False)
    carrera = db.relationship('Carrera', back_populates='egresados')
    experiencias_laborales = db.relationship('ExperienciaLaboral', back_populates='egresado', lazy='dynamic', cascade="all, delete-orphan")
    respuestas = db.relationship('Respuesta', back_populates='egresado', lazy='dynamic', cascade="all, delete-orphan")
    posgrados_asociados = db.relationship('EgresadoPosgrado', back_populates='egresado')
    # --- NUEVA RELACIÓN: Encuestas Asignadas ---
    encuestas_asignadas = db.relationship('EncuestaAsignada', back_populates='egresado', lazy='dynamic', cascade="all, delete-orphan")

    @property
    def display_name(self):
        return f"{self.nombre1} {self.apellido_paterno}"
    @property
    def profile_pic_url(self):
        from flask import url_for, current_app
        if self.foto_perfil_filename and self.foto_perfil_filename != 'default.png':
            rel_path = os.path.join(current_app.config['PROFILE_PICS_FOLDER_REL'], self.foto_perfil_filename)
            return url_for('static', filename=rel_path.replace('\\', '/'))
        else:
            return url_for('static', filename='img/default.png')
    def __repr__(self):
        return f'<Egresado {self.nombre1} {self.apellido_paterno}>'

class PersonalSeguimiento(db.Model):
    # ... (propiedades display_name y profile_pic_url añadidas antes) ...
    __tablename__ = 'personal_seguimiento'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(200), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=True)
    rol = db.Column(db.String(100), nullable=True)
    foto_perfil_filename = db.Column(db.String(100), nullable=True, default='default_staff.png')
    fecha_registro = db.Column(db.DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_login = db.relationship('User', back_populates='perfil_personal', uselist=False)
    noticias_creadas = db.relationship('Noticia', back_populates='autor', lazy='dynamic')
    encuestas_creadas = db.relationship('Encuesta', back_populates='creador', lazy='dynamic')
    @property
    def display_name(self): return f"{self.nombres} {self.apellido_paterno}"
    @property
    def profile_pic_url(self):
        from flask import url_for, current_app
        if self.foto_perfil_filename and self.foto_perfil_filename != 'default_staff.png':
            rel_path = os.path.join(current_app.config['PROFILE_PICS_FOLDER_REL'], self.foto_perfil_filename)
            return url_for('static', filename=rel_path.replace('\\', '/'))
        else: return url_for('static', filename='img/default_staff.png')
    def __repr__(self): return f'<Personal {self.nombres} {self.apellido_paterno}>'

class AutoridadUniversitaria(db.Model):
    # ... (propiedades display_name y profile_pic_url añadidas antes) ...
    __tablename__ = 'autoridad_universitaria'
    id = db.Column(db.Integer, primary_key=True)
    nombre1 = db.Column(db.String(100), nullable=False)
    nombre2 = db.Column(db.String(100), nullable=True)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=True)
    cargo = db.Column(db.String(150), nullable=True)
    id_facultad = db.Column(db.Integer, db.ForeignKey('facultad.id'), nullable=True)
    foto_perfil_filename = db.Column(db.String(100), nullable=True, default='default_staff.png')
    fecha_registro = db.Column(db.DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_login = db.relationship('User', back_populates='perfil_autoridad', uselist=False)
    facultad = db.relationship('Facultad', back_populates='autoridades')
    @property
    def display_name(self): return f"{self.nombre1} {self.apellido_paterno}"
    @property
    def profile_pic_url(self):
        from flask import url_for, current_app
        if self.foto_perfil_filename and self.foto_perfil_filename != 'default_staff.png':
            rel_path = os.path.join(current_app.config['PROFILE_PICS_FOLDER_REL'], self.foto_perfil_filename)
            return url_for('static', filename=rel_path.replace('\\', '/'))
        else: return url_for('static', filename='img/default_staff.png')
    def __repr__(self): return f'<Autoridad {self.cargo} - {self.nombre1} {self.apellido_paterno}>'

# --- TABLA CENTRAL DE LOGIN ---
class User(UserMixin, db.Model):
    # ... (propiedad active_profile añadida antes) ...
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    tipo_usuario = db.Column(db.String(50), nullable=False)
    fecha_creacion = db.Column(db.DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    id_egresado = db.Column(db.Integer, db.ForeignKey('egresado.id'), nullable=True)
    id_personal = db.Column(db.Integer, db.ForeignKey('personal_seguimiento.id'), nullable=True)
    id_autoridad = db.Column(db.Integer, db.ForeignKey('autoridad_universitaria.id'), nullable=True)
    perfil_egresado = db.relationship('Egresado', back_populates='user_login', foreign_keys=[id_egresado])
    perfil_personal = db.relationship('PersonalSeguimiento', back_populates='user_login', foreign_keys=[id_personal])
    perfil_autoridad = db.relationship('AutoridadUniversitaria', back_populates='user_login', foreign_keys=[id_autoridad])
    @property
    def active_profile(self):
        if self.tipo_usuario == 'egresado': return self.perfil_egresado
        elif self.tipo_usuario == 'personal_seguimiento': return self.perfil_personal
        elif self.tipo_usuario == 'autoridad_universitaria': return self.perfil_autoridad # Corregido typo
        return None
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
    def __repr__(self): return f'<User {self.email} ({self.tipo_usuario})>'

@login.user_loader
def load_user(id): return db.session.get(User, int(id))

# --- Tablas de Perfil Adicional (Egresado) ---
class Posgrado(db.Model):
    # ... (sin cambios) ...
    __tablename__ = 'posgrado'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100))
    institucion = db.Column(db.String(200), nullable=False)
    pais = db.Column(db.String(100))
    anio_inicio = db.Column(db.Integer)
    anio_culminacion = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    egresados_asociados = db.relationship('EgresadoPosgrado', back_populates='posgrado')
    def __repr__(self): return f'<Posgrado {self.tipo} en {self.institucion}>'

class ExperienciaLaboral(db.Model):
    # ... (sin cambios) ...
    __tablename__ = 'experiencia_laboral'
    id = db.Column(db.Integer, primary_key=True)
    id_egresado = db.Column(db.Integer, db.ForeignKey('egresado.id'), nullable=False)
    empresa = db.Column(db.String(200), nullable=False)
    puesto = db.Column(db.String(200), nullable=False)
    pais = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date, nullable=True)
    egresado = db.relationship('Egresado', back_populates='experiencias_laborales')
    def __repr__(self): return f'<Experiencia {self.puesto} en {self.empresa}>'

class Noticia(db.Model):
    # ... (sin cambios) ...
    __tablename__ = 'noticia'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.DateTime(timezone=True), server_default=func.now())
    id_autor = db.Column(db.Integer, db.ForeignKey('personal_seguimiento.id'), nullable=False)
    autor = db.relationship('PersonalSeguimiento', back_populates='noticias_creadas')

# --- Módulo de Encuestas ---
class Encuesta(db.Model):
    __tablename__ = 'encuesta'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime(timezone=True), server_default=func.now())
    id_creador = db.Column(db.Integer, db.ForeignKey('personal_seguimiento.id'), nullable=False)

    creador = db.relationship('PersonalSeguimiento', back_populates='encuestas_creadas')
    preguntas = db.relationship('Pregunta', back_populates='encuesta', lazy='dynamic', cascade="all, delete-orphan")
    # --- NUEVA RELACIÓN: Egresados a los que se asignó ---
    asignaciones = db.relationship('EncuestaAsignada', back_populates='encuesta', lazy='dynamic', cascade="all, delete-orphan")

class Pregunta(db.Model):
    # ... (sin cambios) ...
    __tablename__ = 'pregunta'
    id = db.Column(db.Integer, primary_key=True)
    id_encuesta = db.Column(db.Integer, db.ForeignKey('encuesta.id'), nullable=False)
    texto_pregunta = db.Column(db.String(500), nullable=False)
    tipo_pregunta = db.Column(db.String(50), nullable=False)
    encuesta = db.relationship('Encuesta', back_populates='preguntas')
    opciones = db.relationship('OpcionPregunta', back_populates='pregunta', lazy='dynamic', cascade="all, delete-orphan")
    respuestas = db.relationship('Respuesta', back_populates='pregunta', lazy='dynamic', cascade="all, delete-orphan")

class OpcionPregunta(db.Model):
    # ... (sin cambios) ...
    __tablename__ = 'opcion_pregunta'
    id = db.Column(db.Integer, primary_key=True)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable=False)
    texto_opcion = db.Column(db.String(200), nullable=False)
    pregunta = db.relationship('Pregunta', back_populates='opciones')

class Respuesta(db.Model):
    # ... (sin cambios) ...
    __tablename__ = 'respuesta'
    id = db.Column(db.Integer, primary_key=True)
    id_egresado = db.Column(db.Integer, db.ForeignKey('egresado.id'), nullable=False)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable=False)
    fecha_respuesta = db.Column(db.DateTime(timezone=True), server_default=func.now())
    id_opcion = db.Column(db.Integer, db.ForeignKey('opcion_pregunta.id'), nullable=True)
    respuesta_texto = db.Column(db.Text, nullable=True)
    egresado = db.relationship('Egresado', back_populates='respuestas')
    pregunta = db.relationship('Pregunta', back_populates='respuestas')
    opcion = db.relationship('OpcionPregunta')

# --- NUEVA TABLA: Encuesta Asignada ---
class EncuestaAsignada(db.Model):
    __tablename__ = 'encuesta_asignada'
    id = db.Column(db.Integer, primary_key=True)
    id_encuesta = db.Column(db.Integer, db.ForeignKey('encuesta.id'), nullable=False)
    id_egresado = db.Column(db.Integer, db.ForeignKey('egresado.id'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime(timezone=True), server_default=func.now())
    respondida = db.Column(db.Boolean, default=False, nullable=False)
    fecha_respuesta = db.Column(db.DateTime(timezone=True), nullable=True) # Se actualiza cuando responde

    # Relaciones para acceder fácilmente
    encuesta = db.relationship('Encuesta', back_populates='asignaciones')
    egresado = db.relationship('Egresado', back_populates='encuestas_asignadas')

    def __repr__(self):
        return f'<Asignación Encuesta {self.id_encuesta} a Egresado {self.id_egresado}>'
