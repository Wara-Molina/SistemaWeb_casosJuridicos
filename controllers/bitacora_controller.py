from flask import request, redirect, url_for, Blueprint, abort
from models.bitacora_model import Bitacora
from views import bitacora_view

bitacora_bp = Blueprint('bitacora', __name__, url_prefix="/bitacoras")

@bitacora_bp.route("/")
def index():
    bitacoras = Bitacora.get_all()
    return bitacora_view.list(bitacoras)

@bitacora_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        id_usuario = request.form.get('id_usuario')
        accion = request.form.get('accion')
        fecha = request.form.get('fecha')
        Bitacora(id_usuario, accion, fecha).save()
        return redirect(url_for('bitacora.index'))
    return bitacora_view.create()
