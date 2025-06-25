import os
from flask import request, redirect, url_for, Blueprint, abort, current_app
from werkzeug.utils import secure_filename
from flask_login import current_user
from models.seguimiento_model import Seguimiento
from models.caso_model import Caso
from models.usuario_model import Usuario
from views import seguimiento_view
from datetime import datetime

seguimiento_bp = Blueprint('seguimiento', __name__, url_prefix="/seguimientos")

# Protección global para todo el blueprint
@seguimiento_bp.before_request
def verificar_autenticacion():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))  # Ruta de login o inicio

def guardar_archivo(archivo):
    if archivo and archivo.filename != '':
        filename = secure_filename(archivo.filename)
        carpeta_subida = os.path.join(current_app.root_path, 'static/uploads')
        os.makedirs(carpeta_subida, exist_ok=True)
        ruta_completa = os.path.join(carpeta_subida, filename)
        archivo.save(ruta_completa)
        return f'uploads/{filename}'
    return None

@seguimiento_bp.route("/")
def index():
    seguimientos = Seguimiento.get_all()
    return seguimiento_view.list(seguimientos)

@seguimiento_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = request.form
        archivo = request.files.get('archivo')
        archivo_url = guardar_archivo(archivo)

        fecha = datetime.strptime(data['fecha'], "%Y-%m-%d").date()
        proximo_plazo = data.get('proximo_plazo')
        proximo_plazo = datetime.strptime(proximo_plazo, "%Y-%m-%d").date() if proximo_plazo else None

        seguimiento = Seguimiento(
            id_caso=int(data['id_caso']),
            id_usuario=int(data['id_usuario']),
            fecha=fecha,
            descripcion=data['descripcion'],
            archivo_url=archivo_url,
            proximo_plazo=proximo_plazo
        )
        seguimiento.save()
        return redirect(url_for('seguimiento.index'))
    
    casos = Caso.get_all()
    usuarios = Usuario.get_all()
    return seguimiento_view.create(casos=casos, usuarios=usuarios)

@seguimiento_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    seguimiento = Seguimiento.get_by_id(id)
    if not seguimiento:
        abort(404)

    if request.method == 'POST':
        data = request.form
        archivo = request.files.get('archivo')
        archivo_url = guardar_archivo(archivo) or seguimiento.archivo_url

        fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        proximo_plazo = data.get('proximo_plazo')
        proximo_plazo = datetime.strptime(proximo_plazo, '%Y-%m-%d').date() if proximo_plazo else None

        seguimiento.update(
            id_caso=int(data['id_caso']),
            id_usuario=int(data['id_usuario']),
            fecha=fecha,
            descripcion=data['descripcion'],
            archivo_url=archivo_url,
            proximo_plazo=proximo_plazo
        )
        return redirect(url_for('seguimiento.index'))
    
    casos = Caso.get_all()
    usuarios = Usuario.get_all()
    return seguimiento_view.edit(seguimiento, casos=casos, usuarios=usuarios)

@seguimiento_bp.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    seguimiento = Seguimiento.get_by_id(id)
    if not seguimiento:
        abort(404)
    seguimiento.delete()
    return redirect(url_for('seguimiento.index'))