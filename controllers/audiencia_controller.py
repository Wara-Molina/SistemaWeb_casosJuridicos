from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import current_user
from models.audiencia_model import Audiencia
from models.estado_audiencia_model import EstadoAudiencia
from models.caso_model import Caso
from views import audiencia_view
from datetime import datetime

audiencia_bp = Blueprint("audiencia", __name__, url_prefix="/audiencias")

# ✅ Protección global para el Blueprint
@audiencia_bp.before_request
def verificar_autenticacion():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))

@audiencia_bp.route("/")
def index():
    audiencias = Audiencia.get_all()
    return audiencia_view.list(audiencias, id_caso=None)

@audiencia_bp.route("/caso/<int:id_caso>")
def list(id_caso):
    audiencias = Audiencia.get_by_caso(id_caso)
    return audiencia_view.list(audiencias, id_caso)

@audiencia_bp.route("/create/<int:id_caso>", methods=["GET", "POST"])
def create_caso(id_caso):
    if request.method == "POST":
        fecha = request.form.get("fecha_audiencia")
        hora = request.form.get("hora_audiencia")
        lugar = request.form.get("lugar")
        observaciones = request.form.get("observaciones")
        estado_id = request.form.get("id_estado_audiencia")

        audiencia = Audiencia(
            id_caso=id_caso,
            fecha_audiencia=datetime.strptime(fecha, "%Y-%m-%d").date(),
            hora_audiencia=datetime.strptime(hora, "%H:%M").time(),
            lugar=lugar,
            observaciones=observaciones,
            id_estado_audiencia=estado_id,
        )
        audiencia.save()
        return redirect(url_for("audiencia.list", id_caso=id_caso))

    estados = EstadoAudiencia.get_all()
    return audiencia_view.create(id_caso=id_caso, estados=estados)

@audiencia_bp.route("/create", methods=["GET", "POST"])
def create_general():
    if request.method == "POST":
        id_caso = request.form.get("id_caso")
        fecha = request.form.get("fecha_audiencia")
        hora = request.form.get("hora_audiencia")
        lugar = request.form.get("lugar")
        observaciones = request.form.get("observaciones")
        estado_id = request.form.get("id_estado_audiencia")

        audiencia = Audiencia(
            id_caso=int(id_caso),
            fecha_audiencia=datetime.strptime(fecha, "%Y-%m-%d").date(),
            hora_audiencia=datetime.strptime(hora, "%H:%M").time(),
            lugar=lugar,
            observaciones=observaciones,
            id_estado_audiencia=int(estado_id),
        )
        audiencia.save()
        return redirect(url_for("audiencia.index"))

    casos = Caso.get_all()
    estados = EstadoAudiencia.get_all()
    return audiencia_view.create_general(casos=casos, estados=estados)

@audiencia_bp.route("/edit/<int:id_audiencia>", methods=["GET", "POST"])
def edit(id_audiencia):
    audiencia = Audiencia.get_by_id(id_audiencia)
    if not audiencia:
        return "Audiencia no encontrada", 404

    estados = EstadoAudiencia.get_all()

    if request.method == "POST":
        audiencia.update(
            fecha_audiencia=datetime.strptime(request.form.get("fecha_audiencia"), "%Y-%m-%d").date(),
            hora_audiencia=datetime.strptime(request.form.get("hora_audiencia"), "%H:%M").time(),
            lugar=request.form.get("lugar"),
            observaciones=request.form.get("observaciones"),
            id_estado_audiencia=request.form.get("id_estado_audiencia")
        )
        return redirect(url_for("audiencia.list", id_caso=audiencia.id_caso))

    return audiencia_view.edit(audiencia, estados)

@audiencia_bp.route("/delete/<int:id_audiencia>")
def delete(id_audiencia):
    audiencia = Audiencia.get_by_id(id_audiencia)
    if audiencia:
        id_caso = audiencia.id_caso
        audiencia.deactivate()
        return redirect(url_for("audiencia.list", id_caso=id_caso))
    return "Audiencia no encontrada", 404

@audiencia_bp.route("/toggle_activo/<int:id_audiencia>", methods=["POST"])
def toggle_activo(id_audiencia):
    audiencia = Audiencia.get_by_id(id_audiencia)
    if not audiencia:
        return "Audiencia no encontrada", 404

    nuevo_estado = request.form.get("activo") == "on"
    audiencia.activo = nuevo_estado
    audiencia.save()

    return redirect(url_for("audiencia.list", id_caso=audiencia.id_caso))
