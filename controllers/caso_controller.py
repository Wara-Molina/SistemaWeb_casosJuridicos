from flask import Blueprint, request, redirect, url_for, abort
from flask_login import current_user
from models.caso_model import Caso
from views import caso_view
from models.cliente_model import Cliente
from models.usuario_model import Usuario
from models.tipo_caso_model import TipoCaso
from models.estado_caso_model import EstadoCaso
from models.estado_pago_model import EstadoPago
from datetime import datetime

caso_bp = Blueprint('caso', __name__, url_prefix='/casos')

# ✅ Protección global del blueprint: requiere autenticación
@caso_bp.before_request
def verificar_autenticacion():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))

@caso_bp.route('/')
def index():
    # Puedes limitar esto por rol si quieres (ej: secretaria/admin)
    casos = Caso.get_all()
    return caso_view.list(casos)

@caso_bp.route('/create', methods=['GET', 'POST'])
def create():
    # if current_user.rol not in ['Secretaria', 'Administrador']:
    #     abort(403)

    if request.method == 'POST':
        data = request.form
        try:
            fecha_apertura = datetime.strptime(data['fecha_apertura'], '%Y-%m-%d')
        except ValueError:
            fecha_apertura = datetime.now()

        caso = Caso(
            id_cliente=int(data['id_cliente']),
            id_usuario=int(data['id_usuario']),
            id_tipo=int(data['id_tipo']),
            id_estado_caso=int(data['id_estado_caso']),
            fecha_apertura=fecha_apertura,
            descripcion=data.get('descripcion'),
            monto_total=float(data['monto_total']),
            id_estado_pago=int(data['id_estado_pago']),
            activo=data.get('activo', 'on').lower() in ['true', '1', 'on']
        )
        caso.save()
        return redirect(url_for('caso.index'))

    clientes = Cliente.get_all()
    usuarios = Usuario.get_all()
    tipos_caso = TipoCaso.get_all()
    estados_caso = EstadoCaso.get_all()
    estados_pago = EstadoPago.get_all()
    return caso_view.create(clientes=clientes, usuarios=usuarios, tipos_caso=tipos_caso,
                            estados_caso=estados_caso, estados_pago=estados_pago)

@caso_bp.route('/edit/<int:id_caso>', methods=['GET', 'POST'])
def edit(id_caso):
    # if current_user.rol not in ['Secretaria', 'Administrador']:
    #     abort(403)

    caso = Caso.get_by_id(id_caso)
    if not caso:
        abort(404)

    if request.method == 'POST':
        data = request.form
        try:
            fecha_apertura = datetime.strptime(data['fecha_apertura'], '%Y-%m-%d')
        except ValueError:
            fecha_apertura = caso.fecha_apertura

        caso.update(
            id_cliente=int(data['id_cliente']),
            id_usuario=int(data['id_usuario']),
            id_tipo=int(data['id_tipo']),
            id_estado_caso=int(data['id_estado_caso']),
            fecha_apertura=fecha_apertura,
            descripcion=data.get('descripcion'),
            monto_total=float(data['monto_total']),
            id_estado_pago=int(data['id_estado_pago']),
            activo=data.get('activo', 'on').lower() in ['true', '1', 'on']
        )
        return redirect(url_for('caso.index'))

    clientes = Cliente.get_all()
    usuarios = Usuario.get_all()
    tipos_caso = TipoCaso.get_all()
    estados_caso = EstadoCaso.get_all()
    estados_pago = EstadoPago.get_all()
    return caso_view.edit(caso, clientes=clientes, usuarios=usuarios, tipos_caso=tipos_caso,
                          estados_caso=estados_caso, estados_pago=estados_pago)

@caso_bp.route('/delete/<int:id_caso>', methods=['GET', 'POST'])
def delete(id_caso):
    # if current_user.rol not in ['Secretaria', 'Administrador']:
    #     abort(403)

    caso = Caso.get_by_id(id_caso)
    if not caso:
        abort(404)
    caso.delete()
    return redirect(url_for('caso.index'))
