import os
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, abort, current_app
from flask_login import current_user  # <-- Importamos current_user
from werkzeug.utils import secure_filename

from models.documento_model import Documento
from models.caso_model import Caso
from views import documento_view

documento_bp = Blueprint('documento', __name__, url_prefix="/documentos")

# Protección global para todo el blueprint
@documento_bp.before_request
def verificar_autenticacion():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))  # Cambia 'home' por tu ruta de login

def guardar_archivo(archivo):
    if archivo and archivo.filename != '':
        filename = secure_filename(archivo.filename)
        carpeta_subida = os.path.join(current_app.root_path, 'static/uploads')
        os.makedirs(carpeta_subida, exist_ok=True)
        ruta_completa = os.path.join(carpeta_subida, filename)
        archivo.save(ruta_completa)
        return f'uploads/{filename}'  # Ruta relativa
    return None

@documento_bp.route("/")
def index():
    documentos = Documento.get_all()
    return documento_view.list(documentos)

@documento_bp.route("/create", methods=['GET', 'POST'])
def create():
    casos = Caso.get_all()
    if request.method == 'POST':
        data = request.form
        archivo = request.files.get('archivo')
        archivo_path = guardar_archivo(archivo)

        documento = Documento(
            id_caso=int(data['id_caso']),
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            archivo_path=archivo_path,
            fecha_subida=datetime.now()
        )
        documento.save()
        return redirect(url_for('documento.index'))
    return documento_view.create(casos=casos)

@documento_bp.route("/edit/<int:id_documento>", methods=['GET', 'POST'])
def edit(id_documento):
    documento = Documento.get_by_id(id_documento)
    if not documento:
        abort(404)
    casos = Caso.get_all()
    if request.method == 'POST':
        data = request.form
        archivo = request.files.get('archivo')
        archivo_path = guardar_archivo(archivo) or documento.archivo_path

        documento.update(
            id_caso=int(data['id_caso']),
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            archivo_path=archivo_path,
            fecha_subida=datetime.now()  # Actualiza fecha si deseas
        )
        return redirect(url_for('documento.index'))
    return documento_view.edit(documento, casos=casos)

@documento_bp.route("/delete/<int:id_documento>", methods=['POST'])
def delete(id_documento):
    documento = Documento.get_by_id(id_documento)
    if not documento:
        abort(404)
    documento.delete()
    return redirect(url_for('documento.index'))
