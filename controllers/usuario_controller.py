from flask import request, redirect, url_for, Blueprint, abort, flash
from flask_login import current_user
from models.usuario_model import Usuario
from models.rol_model import Rol
from models.estado_usuario_model import EstadoUsuario
from models.especialidad_model import Especialidad
from views import usuario_view

usuario_bp = Blueprint('usuario', __name__, url_prefix="/usuarios")

# ✅ Protección global del blueprint
@usuario_bp.before_request
def verificar_acceso():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    if current_user.rol != 'Administrador':
        flash("Acceso no autorizado", "danger")
        return redirect(url_for('home'))

@usuario_bp.route("/")
def index():
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)

@usuario_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = request.form
        rol_id = int(data.get('id_rol'))
        rol = Rol.get_by_id(rol_id)

        matricula = data.get('matricula')
        id_especialidad = data.get('id_especialidad')

        # Validar si el rol requiere matrícula y especialidad
        if rol and rol.nombre_rol.lower() == "abogado":
            if not matricula or not id_especialidad:
                flash("Los campos Matrícula y Especialidad son obligatorios para el rol Abogado.", "danger")
                return redirect(url_for('usuario.create'))
        else:
            matricula = None
            id_especialidad = None

        usuario = Usuario(
            nombre=data.get('nombre'),
            usuario=data.get('usuario'),
            password=data.get('password'),
            telefono=data.get('telefono'),
            direccion=data.get('direccion'),
            matricula=matricula,
            id_especialidad=id_especialidad,
            id_rol=rol_id,
            id_estado_usuario=int(data.get('id_estado_usuario')),
            activo=data.get('activo', 'off').lower() in ['true', '1', 'on']
        )
        usuario.save()
        return redirect(url_for('usuario.index'))

    roles = Rol.get_all()
    estado_usuarios = EstadoUsuario.get_all()
    especialidades = Especialidad.get_all()
    return usuario_view.create(roles=roles, estado_usuarios=estado_usuarios, especialidades=especialidades)

@usuario_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    usuario = Usuario.get_by_id(id)
    if not usuario:
        abort(404)

    if request.method == 'POST':
        data = request.form
        rol_id = int(data.get('id_rol'))
        rol = Rol.get_by_id(rol_id)

        matricula = data.get('matricula')
        id_especialidad = data.get('id_especialidad')

        if rol and rol.nombre_rol.lower() == "abogado":
            if not matricula or not id_especialidad:
                flash("Los campos Matrícula y Especialidad son obligatorios para el rol Abogado.", "danger")
                return redirect(url_for('usuario.edit', id=id))
        else:
            matricula = None
            id_especialidad = None

        usuario.update(
            nombre=data.get('nombre'),
            usuario=data.get('usuario'),
            password=data.get('password'),
            telefono=data.get('telefono'),
            direccion=data.get('direccion'),
            matricula=matricula,
            id_rol=rol_id,
            id_estado_usuario=int(data.get('id_estado_usuario')),
            id_especialidad=id_especialidad,
            activo=data.get('activo', 'off').lower() in ['true', '1', 'on']
        )
        return redirect(url_for('usuario.index'))

    roles = Rol.get_all()
    estado_usuarios = EstadoUsuario.get_all()
    especialidades = Especialidad.get_all()
    return usuario_view.edit(usuario, roles=roles, estado_usuarios=estado_usuarios, especialidades=especialidades)

@usuario_bp.route("/delete/<int:id_usuario>", methods=['GET', 'POST'])
def delete(id_usuario):
    usuario = Usuario.get_by_id(id_usuario)
    if not usuario:
        abort(404)
    usuario.delete()
    return redirect(url_for('usuario.index'))
