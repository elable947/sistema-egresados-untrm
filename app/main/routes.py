# -*- coding: utf-8 -*-
from flask import render_template
from flask_login import login_required
from app.main import bp

@bp.route('/')
@bp.route('/index')
@login_required # ¡Protegido! El usuario debe estar logueado.
def index():
    """
    Página principal (Dashboard) después del login.
    Por ahora, solo muestra un saludo.
    """
    # Crearemos 'main/index.html' después.
    return render_template('main/index.html', title='Inicio')
