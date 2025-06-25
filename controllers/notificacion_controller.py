from flask import Blueprint, request, redirect, url_for, abort, session
from models.notificacion_model import Notificacion
from views import notificacion_view
from datetime import datetime

notificacion_bp = Blueprint('notificacion', __name__, url_prefix="/notificaciones")

@notificacion_bp.route("/")
def index():
    if 'id_usuario' not in session:
        abort(401)
    notificaciones = Notificacion.query.filter_by(id_usuario=session['id_usuario']).all()
    return notificacion_view.list(notificaciones)

@notificacion_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        if 'id_usuario' not in session:
            abort(401)
        mensaje = request.form.get('mensaje')
        fecha = datetime.now()
        notificacion = Notificacion(
            id_usuario=session['id_usuario'],
            mensaje=mensaje,
            fecha=fecha,
            leido=False
        )
        notificacion.save()
        return redirect(url_for('notificacion.index'))
    return notificacion_view.create()

@notificacion_bp.route("/edit/<int:id_notificacion>", methods=['GET', 'POST'])
def edit(id_notificacion):
    notificacion = Notificacion.get_by_id(id_notificacion)
    if not notificacion:
        abort(404)
    if 'id_usuario' not in session or notificacion.id_usuario != session['id_usuario']:
        abort(403)

    if request.method == 'POST':
        mensaje = request.form.get('mensaje')
        notificacion.update(mensaje=mensaje)
        return redirect(url_for('notificacion.index'))

    return notificacion_view.edit(notificacion)

@notificacion_bp.route("/delete/<int:id_notificacion>", methods=['POST'])
def delete(id_notificacion):
    notificacion = Notificacion.get_by_id(id_notificacion)
    if not notificacion:
        abort(404)
    if 'id_usuario' not in session or notificacion.id_usuario != session['id_usuario']:
        abort(403)
    notificacion.delete()
    return redirect(url_for('notificacion.index'))

@notificacion_bp.route("/mark_read/<int:id_notificacion>", methods=['POST'])
def mark_read(id_notificacion):
    notificacion = Notificacion.get_by_id(id_notificacion)
    if not notificacion:
        abort(404)
    if 'id_usuario' not in session or notificacion.id_usuario != session['id_usuario']:
        abort(403)
    notificacion.update(leido=True)
    return redirect(url_for('notificacion.index'))