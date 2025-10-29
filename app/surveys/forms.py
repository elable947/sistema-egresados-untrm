from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateSurveyForm(FlaskForm):
    """Formulario para crear una nueva encuesta."""
    titulo = StringField(
        'Título de la Encuesta',
        validators=[DataRequired(message="El título es obligatorio."), Length(min=5, max=250)]
    )
    descripcion = TextAreaField(
        'Descripción (Opcional)',
        validators=[Length(max=1000)]
    )
    submit = SubmitField('Crear Encuesta')

# --- Más adelante añadiremos formularios para añadir preguntas ---
# class AddQuestionForm(FlaskForm):
#    ...
