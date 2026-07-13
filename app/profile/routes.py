import os
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename # Para nombres de archivo seguros
from app import db
from app.profile import bp
from app.profile.forms import EditProfileForm, WorkExperienceForm
from app.models import Egresado, ExperienciaLaboral # Asegúrate de importar ExperienciaLaboral

    # Helper function para verificar extensiones permitidas
def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    # Ruta principal del perfil
@bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def view_profile():
        # Asegurarnos de que el usuario actual tenga un perfil de egresado asociado
        if not current_user.perfil_egresado:
            flash('Error: No se encontró el perfil de egresado asociado a este usuario.', 'danger')
            return redirect(url_for('main.index'))

        egresado = current_user.perfil_egresado

        # Creamos ambos formularios
        profile_form = EditProfileForm(obj=egresado) # Carga datos existentes en el GET
        work_form = WorkExperienceForm()
        work_form_errors = None # Para pasar errores del work_form a la plantilla

        # Manejar el envío del formulario de EDICIÓN DE PERFIL (POST)
        # Usamos el nombre del botón submit para diferenciar
        if profile_form.validate_on_submit() and profile_form.submit_profile.data:
            # --- Lógica para SUBIR FOTO ---
            if profile_form.foto.data: # Si se subió un archivo
                file = profile_form.foto.data
                if file and allowed_file(file.filename):
                    # Generar un nombre de archivo seguro y único (ej. user_1_uuid.jpg)
                    filename = secure_filename(f"user_{current_user.id}_{file.filename}") # Podríamos añadir un UUID para más unicidad
                    # Usamos la ruta ABSOLUTA para guardar
                    save_path = os.path.join(current_app.config['PROFILE_PICS_FOLDER_ABS'], filename)
                    try:
                        file.save(save_path)
                        # Actualizar el nombre del archivo en la BD
                        egresado.foto_perfil_filename = filename
                        flash('Foto de perfil actualizada con éxito.', 'success')
                    except Exception as e:
                        flash(f'Error al guardar la foto: {e}', 'danger')
                elif file.filename != '':
                    flash('Tipo de archivo no permitido. Sube png, jpg, jpeg o gif.', 'warning')


            # Actualizar otros campos del egresado
            egresado.telefono = profile_form.telefono.data
            egresado.pais_residencia = profile_form.pais_residencia.data
            egresado.ciudad_residencia = profile_form.ciudad_residencia.data
            egresado.direccion = profile_form.direccion.data
            egresado.fecha_nacimiento = profile_form.fecha_nacimiento.data
            egresado.perfil_publico = profile_form.perfil_publico.data
            egresado.mostrar_email_publico = profile_form.mostrar_email_publico.data

            try:
                db.session.commit() # Guardamos todos los cambios (incluida la foto si se actualizó)
                flash('Tu información personal ha sido actualizada.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar el perfil: {e}', 'danger')

            return redirect(url_for('profile.view_profile')) # Redirigir siempre después de un POST exitoso

        # Rellenar el formulario de perfil con datos existentes (GET)
        # Si no es un POST, o si el POST falló la validación (se maneja por WTForms),
        # rellenamos el formulario con los datos actuales de la BD para mostrarlo.
        # WTForms lo hace automáticamente con obj=egresado, pero lo hacemos explícito para claridad
        elif request.method == 'GET':
            profile_form.telefono.data = egresado.telefono
            profile_form.pais_residencia.data = egresado.pais_residencia
            profile_form.ciudad_residencia.data = egresado.ciudad_residencia
            profile_form.direccion.data = egresado.direccion
            profile_form.fecha_nacimiento.data = egresado.fecha_nacimiento
            profile_form.perfil_publico.data = egresado.perfil_publico
            profile_form.mostrar_email_publico.data = egresado.mostrar_email_publico

        # Cargar las experiencias laborales existentes para mostrarlas
        # Usamos .all() aquí porque las necesitamos iterar en la plantilla
        experiencias = egresado.experiencias_laborales.order_by(ExperienciaLaboral.fecha_inicio.desc()).all()


        # Renderizar la plantilla HTML
        return render_template('profile/perfil.html',
                               title='Mi Información',
                               profile_form=profile_form,
                               work_form=work_form,
                               experiencias=experiencias,
                               egresado=egresado, # Pasamos el objeto egresado completo
                               work_form_errors=work_form_errors)


    # Ruta dedicada al POST del formulario de AÑADIR experiencia laboral
@bp.route('/perfil/work/add', methods=['POST'])
@login_required
def add_work():
        # Asegurarnos de que el usuario actual tenga un perfil de egresado
        if not current_user.perfil_egresado:
            flash('Error: No se encontró el perfil de egresado.', 'danger')
            return redirect(url_for('main.index'))

        # Creamos el formulario de experiencia laboral
        work_form = WorkExperienceForm()

        if work_form.validate_on_submit(): # Ya no necesitamos chequear el botón submit_work.data
            # Creamos el nuevo objeto de ExperienciaLaboral
            nueva_experiencia = ExperienciaLaboral(
                empresa=work_form.empresa.data,
                puesto=work_form.puesto.data,
                pais=work_form.pais.data,
                sector=work_form.sector.data,
                fecha_inicio=work_form.fecha_inicio.data,
                fecha_fin=work_form.fecha_fin.data,
                id_egresado=current_user.perfil_egresado.id # Vinculamos al egresado logueado
            )
            try:
                db.session.add(nueva_experiencia)
                db.session.commit()
                flash('¡Experiencia laboral añadida exitosamente!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al guardar la experiencia laboral: {e}', 'danger')
            # Redirigimos de vuelta a la página de perfil principal
            return redirect(url_for('profile.view_profile'))
        else:
            # Si el formulario no es válido (ej. falta un campo),
            # necesitamos re-renderizar la página de perfil mostrando los errores.
            # Pasamos los errores del work_form a la plantilla view_profile.
            # Volvemos a cargar los datos necesarios para view_profile.
            profile_form = EditProfileForm(obj=current_user.perfil_egresado)
            experiencias = current_user.perfil_egresado.experiencias_laborales.order_by(ExperienciaLaboral.fecha_inicio.desc()).all()
            # Convertimos los errores a un formato más simple si es necesario o los pasamos directamente
            work_form_errors = work_form.errors # Pasamos el diccionario de errores

            flash('Error en el formulario de experiencia laboral. Por favor, revisa los campos.', 'danger')

            return render_template('profile/perfil.html',
                                   title='Mi Información',
                                   profile_form=profile_form,
                                   work_form=work_form, # Pasamos el work_form con los datos ingresados y errores
                                   experiencias=experiencias,
                                   egresado=current_user.perfil_egresado,
                                   work_form_errors=work_form_errors) # Pasamos los errores explícitamente


