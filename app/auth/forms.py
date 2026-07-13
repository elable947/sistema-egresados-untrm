# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    """
    Formulario para el inicio de sesión del usuario.
    Basado en la imagen de referencia (Correo + Contraseña).
    """
    email = StringField(
        'Correo Electrónico', 
        validators=[
            DataRequired(message='El correo es obligatorio.'), 
            Email(message='Correo electrónico no válido.')
        ]
    )
    
    password = PasswordField(
        'Contraseña', 
        validators=[
            DataRequired(message='La contraseña es obligatoria.')
        ]
    )
    
    remember_me = BooleanField('Recordarme')
    
    submit = SubmitField('Iniciar Sesión')