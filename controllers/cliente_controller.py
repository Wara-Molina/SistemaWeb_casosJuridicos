from flask import request, redirect, url_for, Blueprint, abort
from flask_login import current_user
from models.cliente_model import Cliente
from views import cliente_view

cliente_bp = Blueprint('cliente', __name__, url_prefix="/clientes")

# ✅ Protección global para todo el Blueprint
@cliente_bp.before_request
def verificar_autenticacion():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))

@cliente_bp.route("/")
def index():
    if current_user.rol not in ['Secretaria', 'Administrador']:
        abort(403)
    clientes = Cliente.get_all()
    return cliente_view.list(clientes)

@cliente_bp.route("/abogado")
def index_abogado():
    if current_user.rol != 'Abogado':
        abort(403)
    clientes = Cliente.get_by_abogado(current_user.id) if hasattr(Cliente, 'get_by_abogado') else Cliente.get_all()
    return cliente_view.list_abogado(clientes)

@cliente_bp.route("/create", methods=['GET', 'POST'])
def create():
    if current_user.rol not in ['Secretaria', 'Abogado']:
        abort(403)

    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        activo = request.form['activo'].lower() in ['true', '1', 'on']

        cliente = Cliente(nombre, cedula, direccion, telefono, email, activo)
        cliente.save()

        if current_user.rol == 'Abogado':
            return redirect(url_for('cliente.index_abogado'))
        else:
            return redirect(url_for('cliente.index'))

    return cliente_view.create()

@cliente_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    if current_user.rol not in ['Secretaria', 'Administrador']:
        abort(403)

    cliente = Cliente.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        activo = request.form['activo'].lower() in ['true', '1', 'on']

        cliente.update(nombre=nombre, cedula=cedula, direccion=direccion,
                       telefono=telefono, email=email, activo=activo)

        return redirect(url_for('cliente.index'))

    return cliente_view.edit(cliente)

@cliente_bp.route("/delete/<int:id>")
def delete(id):
    if current_user.rol not in ['Secretaria', 'Administrador']:
        abort(403)

    cliente = Cliente.get_by_id(id)
    if not cliente:
        return "Cliente no encontrado", 404

    cliente.delete()
    return redirect(url_for('cliente.index'))
