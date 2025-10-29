from flask import current_app # Necesitamos importar current_app aquí
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # Importamos FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import Optional, Length

class EditGenericProfileForm(FlaskForm):
    """Formulario para editar datos básicos de Personal y Autoridad."""
    nombres = StringField(
        'Nombres',
        validators=[Optional(), Length(max=200)]
    )
    apellido_paterno = StringField(
        'Apellido Paterno',
        validators=[Optional(), Length(max=100)]
    )
    apellido_materno = StringField(
        'Apellido Materno',
        validators=[Optional(), Length(max=100)]
    )
    # --- CAMBIO: Definimos 'foto' SIN FileAllowed inicialmente ---
    foto = FileField(
        'Cambiar Foto de Perfil (Opcional)',
        validators=[Optional()] # Solo Optional por ahora
    )
    submit = SubmitField('Actualizar Perfil')

    # --- CAMBIO: Modificamos __init__ ---
    def __init__(self, original_profile_obj, *args, **kwargs):
        super(EditGenericProfileForm, self).__init__(*args, **kwargs)
        self.original_profile_obj = original_profile_obj

        # --- CAMBIO: Añadimos FileAllowed dinámicamente ---
        # Ahora sí podemos acceder a current_app.config de forma segura
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
        self.foto.validators.append(
            FileAllowed(allowed_extensions, '¡Solo imágenes (png, jpg, jpeg, gif)!')
        )

        # Mantenemos la lógica para ocultar campos
        if not hasattr(original_profile_obj, 'nombres'):
             # Si el objeto original no tiene 'nombres', quitamos el campo del form
             # Usamos try/except por si el campo ya fue eliminado
             try:
                 del self.nombres
             except AttributeError:
                 pass
        # Similar para 'nombre1' si lo añadiéramos para Autoridad
        # if not hasattr(original_profile_obj, 'nombre1'):
        #     try:
        #         del self.nombre1
        #     except AttributeError:


