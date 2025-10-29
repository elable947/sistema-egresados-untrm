   # -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, Optional, ValidationError
from flask_wtf.file import FileAllowed # Importamos FileAllowed
   # Podríamos importar el modelo User para validaciones si fuera necesario
   # from app.models import User

   # Formulario para editar el perfil básico del egresado
class EditProfileForm(FlaskForm):
       telefono = StringField('Teléfono/Celular', validators=[Optional(), Length(min=6, max=20)])
       fecha_nacimiento = DateField('Fecha de Nacimiento (Opcional)', validators=[Optional()])
       pais_residencia = StringField('País de Residencia Actual', validators=[Optional(), Length(max=100)])
       ciudad_residencia = StringField('Ciudad de Residencia Actual', validators=[Optional(), Length(max=100)])
       direccion = StringField('Dirección (Opcional)', validators=[Optional(), Length(max=255)])

       # --- NUEVO CAMPO PARA SUBIR FOTO ---
       foto = FileField('Foto de Perfil (Opcional)', validators=[
           FileAllowed(['jpg', 'png', 'jpeg', 'gif'], '¡Solo imágenes (.jpg, .png, .jpeg, .gif)!')
       ])

       # Opciones de privacidad para Networking
       perfil_publico = BooleanField('Hacer mi perfil visible en el directorio de Networking')
       mostrar_email_publico = BooleanField('Permitir que otros egresados vean mi correo de contacto')

       submit_profile = SubmitField('Actualizar Datos Personales')

   # Formulario para añadir una nueva experiencia laboral
class WorkExperienceForm(FlaskForm):
       empresa = StringField('Empresa', validators=[DataRequired(), Length(max=200)])
       puesto = StringField('Puesto/Cargo', validators=[DataRequired(), Length(max=200)])
       pais = StringField('País', validators=[Optional(), Length(max=100)])
       sector = StringField('Sector', validators=[Optional(), Length(max=100)]) # Ej. Tecnología, Educación
       fecha_inicio = DateField('Fecha Inicio', validators=[DataRequired()])
       fecha_fin = DateField('Fecha Fin (Dejar en blanco si es actual)', validators=[Optional()])
       submit_work = SubmitField('Guardar Experiencia Laboral')


