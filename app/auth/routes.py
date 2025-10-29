# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User
from app import db
from urllib.parse import urlsplit

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Lógica para la vista de /login.
    Muestra el formulario y procesa el inicio de sesión.
    """
    # Si el usuario ya está autenticado, redirigir a la página principal
    if current_user.is_authenticated:
        # 'main.index' será nuestra ruta principal (la creamos después)
        return redirect(url_for('main.index'))

    form = LoginForm()
    
    # Si el formulario es válido (se envió un POST y pasó las validaciones)
    if form.validate_on_submit():
        # 1. Buscar al usuario en la BD por su email
        user = db.session.scalar(
            db.select(User).where(User.email == form.email.data)
        )

        # 2. Verificar si el usuario no existe O la contraseña es incorrecta
        if user is None or not user.check_password(form.password.data):
            flash('Correo electrónico o contraseña inválidos.', 'danger')
            return redirect(url_for('auth.login'))

        # 3. Registrar al usuario como "logueado"
        login_user(user, remember=form.remember_me.data)
        
        # 4. Redirección segura
        # Si el usuario intentó acceder a una página protegida (@login_required),
        # Flask guarda esa URL en request.args.get('next').
        next_page = request.args.get('next')
        
        # Si no hay 'next_page' O si 'next_page' es un enlace a otro sitio (peligroso),
        # redirigir a la página principal.
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index') # 'main.index' es el dashboard
        
        flash(f'¡Bienvenido de vuelta!', 'success')
        return redirect(next_page)

    # Si es un GET o el formulario no es válido, mostrar la plantilla HTML
    # Crearemos 'auth/login.html' en el siguiente paso.
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

@bp.route('/logout')
@login_required # Solo un usuario logueado puede desloguearse
def logout():
    """
    Lógica para la vista de /logout.
    """
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login')) # Enviar de vuelta al login
