from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app import db
from app.surveys import bp
from app.surveys.forms import CreateSurveyForm
from app.models import Encuesta, User, Egresado, Carrera, Facultad, EncuestaAsignada, PersonalSeguimiento # Asegúrate de importar PersonalSeguimiento

# --- Decorador simple para verificar rol ---
from functools import wraps
def personal_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo_usuario != 'personal_seguimiento':
            abort(403) # Forbidden
        return f(*args, **kwargs)
    return decorated_function

# --- NUEVO: Decorador para verificar rol Egresado ---
def egresado_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo_usuario != 'egresado':
            abort(403) # Forbidden
        return f(*args, **kwargs)
    return decorated_function
# --------------------------------------------------

@bp.route('/encuestas')
@login_required
@personal_required
def list_surveys():
    """Muestra la lista de encuestas creadas (Vista Personal)."""
    encuestas = Encuesta.query.order_by(Encuesta.fecha_creacion.desc()).all()
    return render_template('list_surveys.html', title='Gestión de Encuestas', encuestas=encuestas)

@bp.route('/encuestas/crear', methods=['GET', 'POST'])
@login_required
@personal_required
def create_survey():
    """Muestra el formulario para crear una nueva encuesta y la procesa (Vista Personal)."""
    form = CreateSurveyForm()
    if not current_user.id_personal:
         flash('Error: Tu usuario no está correctamente vinculado a un perfil de personal.', 'danger')
         return redirect(url_for('surveys.list_surveys'))

    if form.validate_on_submit():
        nueva_encuesta = Encuesta(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            id_creador=current_user.id_personal
        )
        try:
            db.session.add(nueva_encuesta)
            db.session.commit()
            flash('¡Encuesta creada exitosamente!', 'success')
            return redirect(url_for('surveys.list_surveys'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la encuesta: {e}', 'danger')
    return render_template('create_survey.html', title='Crear Nueva Encuesta', form=form)


@bp.route('/encuestas/<int:survey_id>/enviar', methods=['GET', 'POST'])
@login_required
@personal_required
def send_survey_view(survey_id):
    """Muestra la interfaz para seleccionar egresados y enviarles la encuesta (Vista Personal)."""
    encuesta = db.session.get(Encuesta, survey_id)
    if not encuesta: abort(404)

    facultades = Facultad.query.order_by(Facultad.nombre).all()
    carreras_query = Carrera.query # Empezamos con todas
    selected_facultad_id = request.args.get('facultad', type=int)
    selected_carrera_id = request.args.get('carrera', type=int)
    search_term = request.args.get('search', '')

    query_egresados = Egresado.query.join(Carrera).join(Facultad)

    if selected_facultad_id:
        query_egresados = query_egresados.filter(Facultad.id == selected_facultad_id)
        carreras_query = carreras_query.filter(Carrera.id_facultad == selected_facultad_id)

    if selected_carrera_id:
        query_egresados = query_egresados.filter(Carrera.id == selected_carrera_id)

    if search_term:
        search_like = f"%{search_term}%"
        query_egresados = query_egresados.filter(
            db.or_( Egresado.nombre1.ilike(search_like), Egresado.apellido_paterno.ilike(search_like), Egresado.apellido_materno.ilike(search_like) )
        )

    egresados_filtrados = query_egresados.order_by(Egresado.apellido_paterno, Egresado.nombre1).all()
    carreras = carreras_query.order_by(Carrera.nombre).all() # Obtenemos las carreras filtradas

    if request.method == 'POST':
        selected_egresado_ids = request.form.getlist('egresado_ids')
        if not selected_egresado_ids:
            flash('Debes seleccionar al menos un egresado.', 'warning')
        else:
            try:
                count = 0
                for egresado_id in selected_egresado_ids:
                    existe = EncuestaAsignada.query.filter_by(id_encuesta=survey_id, id_egresado=egresado_id).first()
                    if not existe:
                        asignacion = EncuestaAsignada(id_encuesta=survey_id, id_egresado=int(egresado_id))
                        db.session.add(asignacion)
                        count += 1
                if count > 0: # Solo commit si hubo nuevas asignaciones
                    db.session.commit()
                    flash(f'Encuesta asignada a {count} nuevo(s) egresado(s) exitosamente.', 'success')
                else:
                    flash('No se asignaron nuevas encuestas (posiblemente ya estaban asignadas).', 'info')

                return redirect(url_for('surveys.send_survey_view', survey_id=survey_id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al asignar la encuesta: {e}', 'danger')

    return render_template('send_survey.html',
                           title=f'Enviar Encuesta: {encuesta.titulo}',
                           encuesta=encuesta, facultades=facultades, carreras=carreras,
                           egresados=egresados_filtrados, selected_facultad_id=selected_facultad_id,
                           selected_carrera_id=selected_carrera_id, search_term=search_term)


# --- NUEVA RUTA: Mis Encuestas (Vista Egresado) ---
@bp.route('/mis-encuestas')
@login_required
@egresado_required # Solo egresados pueden ver esto
def my_surveys():
    """Muestra las encuestas asignadas al egresado actual."""
    if not current_user.id_egresado:
         flash('Error: Tu usuario no está vinculado a un perfil de egresado.', 'danger')
         return redirect(url_for('main.index'))

    # Buscamos las asignaciones para el egresado actual, haciendo join para obtener info de la encuesta y su creador
    asignaciones = EncuestaAsignada.query.filter_by(id_egresado=current_user.id_egresado)\
                     .join(EncuestaAsignada.encuesta)\
                     .join(Encuesta.creador)\
                     .options(db.contains_eager(EncuestaAsignada.encuesta).contains_eager(Encuesta.creador))\
                     .order_by(EncuestaAsignada.fecha_asignacion.desc())\
                     .all()

    return render_template('my_surveys.html', title='Mis Encuestas', asignaciones=asignaciones)

# --- (Rutas futuras para ver/editar encuesta, añadir preguntas, responder encuesta...) ---

