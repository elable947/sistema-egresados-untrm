import os
from flask import render_template, flash, redirect, url_for, current_app, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.user_settings import bp
from app.user_settings.forms import EditGenericProfileForm

# Helper para guardar fotos
def save_profile_picture(photo_file):
    filename = secure_filename(photo_file.filename)
    # Genera un nombre único con el ID de usuario para evitar colisiones
    ext = os.path.splitext(filename)[1] # Obtiene la extensión
    new_filename = f"user_{current_user.id}_{os.urandom(8).hex()}{ext}"
    picture_path = os.path.join(current_app.config['PROFILE_PICS_FOLDER_ABS'], new_filename)

    # Guarda el archivo
    photo_file.save(picture_path)
    return new_filename

@bp.route('/mi-perfil', methods=['GET', 'POST'])
@login_required
def my_profile():
    # Aseguramos que solo el Personal de Seguimiento o Autoridad pueda acceder a esta ruta
    if current_user.tipo_usuario not in ['personal_seguimiento', 'autoridad_universitaria']:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('main.index'))

    profile = current_user.active_profile
    if not profile:
        flash('No se encontró el perfil asociado a tu cuenta.', 'danger')
        return redirect(url_for('main.index'))

    form = EditGenericProfileForm(original_profile_obj=profile)

    if form.validate_on_submit():
        if form.nombres and hasattr(profile, 'nombres'): # Solo actualiza si el campo existe en el formulario y el modelo
            profile.nombres = form.nombres.data
        if form.apellido_paterno and hasattr(profile, 'apellido_paterno'):
            profile.apellido_paterno = form.apellido_paterno.data
        if form.apellido_materno and hasattr(profile, 'apellido_materno'):
            profile.apellido_materno = form.apellido_materno.data

        if form.foto.data:
            # Eliminar la foto anterior si existe y no es la por defecto
            if profile.foto_perfil_filename and \
               profile.foto_perfil_filename not in ['default.png', 'default_staff.png']:
                old_pic_path = os.path.join(current_app.config['PROFILE_PICS_FOLDER_ABS'], profile.foto_perfil_filename)
                if os.path.exists(old_pic_path):
                    os.remove(old_pic_path)

            picture_file = form.foto.data
            profile.foto_perfil_filename = save_profile_picture(picture_file)
        
        db.session.commit()
        flash('Tu perfil ha sido actualizado exitosamente.', 'success')
        return redirect(url_for('user_settings.my_profile'))
    elif request.method == 'GET':
        if hasattr(profile, 'nombres'):
            form.nombres.data = profile.nombres
        if hasattr(profile, 'apellido_paterno'):
            form.apellido_paterno.data = profile.apellido_paterno
        if hasattr(profile, 'apellido_materno'):
            form.apellido_materno.data = profile.apellido_materno
    
    # Obtener la URL de la foto de perfil actual para mostrarla
    profile_image_url = profile.profile_pic_url # Usa la propiedad del modelo

    return render_template('user_settings/my_profile.html', title='Mi Perfil', form=form, profile_image_url=profile_image_url)

