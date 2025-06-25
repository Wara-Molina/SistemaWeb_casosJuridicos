from flask import request, redirect, url_for, Blueprint, abort, flash
from flask_login import current_user
from datetime import datetime
from decimal import Decimal
from models.pago_model import Pago
from models.estado_pago_model import EstadoPago
from models.caso_model import Caso 
from models.cliente_model import Cliente
from views import pago_view

pago_bp = Blueprint('pago', __name__, url_prefix="/pagos")

# ✅ Protección global del Blueprint
@pago_bp.before_request
def verificar_autenticacion():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))

@pago_bp.route("/")
def index():
    pagos = Pago.get_all()
    return pago_view.list(pagos)

@pago_bp.route("/create", methods=['GET', 'POST'])
def create():
    estados = EstadoPago.get_all()
    casos = Caso.get_all()
    clientes = Cliente.get_all() 

    if request.method == 'POST':
        data = request.form
        fecha = datetime.strptime(data['fecha_pago'], '%Y-%m-%d').date()
        monto = Decimal(str(data['monto_pagado']))
        id_caso = int(data['id_caso'])
        id_cliente = int(data['id_cliente'])

        caso = Caso.query.get(id_caso)
        if not caso:
            flash("El caso no existe", "danger")
            return redirect(url_for('pago.create'))

        if monto > caso.saldo_restante:
            flash(f"El monto supera el saldo restante del caso (Bs. {caso.saldo_restante})", "danger")
            return redirect(url_for('pago.create'))

        pago = Pago(
            id_cliente=id_cliente, 
            id_caso=id_caso,
            fecha_pago=fecha,
            monto_pagado=monto,
            metodo_pago=data.get('metodo_pago'),
            observaciones=data.get('observaciones'),
            id_estado_pago=int(data.get('id_estado_pago')) if data.get('id_estado_pago') else None
        )

        pago.save()
        flash(f"Pago registrado correctamente por Bs. {monto:.2f}", "success")
        return redirect(url_for('pago.index'))

    return pago_view.create(estados=estados, casos=casos, clientes=clientes) 

@pago_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    pago = Pago.get_by_id(id)
    if not pago:
        abort(404)

    estados = EstadoPago.get_all()
    casos = Caso.get_all()
    clientes = Cliente.get_all() 

    if request.method == 'POST':
        data = request.form
        fecha = datetime.strptime(data['fecha_pago'], '%Y-%m-%d').date()
        nuevo_monto = Decimal(str(data['monto_pagado']))
        id_caso = int(data['id_caso'])
        id_cliente = int(data['id_cliente']) 

        caso = Caso.query.get(id_caso)
        if not caso:
            flash("El caso no existe", "danger")
            return redirect(url_for('pago.edit', id=id))

        saldo_actual = caso.saldo_restante + pago.monto_pagado
        if nuevo_monto > saldo_actual:
            flash(f"El nuevo monto supera el saldo permitido (máximo Bs. {saldo_actual})", "danger")
            return redirect(url_for('pago.edit', id=id))

        pago.update(
            id_cliente=id_cliente, 
            id_caso=id_caso,
            fecha_pago=fecha,
            monto_pagado=nuevo_monto,
            metodo_pago=data.get('metodo_pago'),
            observaciones=data.get('observaciones'),
            id_estado_pago=int(data.get('id_estado_pago')) if data.get('id_estado_pago') else None
        )

        flash("Pago actualizado correctamente", "success")
        return redirect(url_for('pago.index'))

    return pago_view.edit(pago, estados=estados, casos=casos, clientes=clientes)

@pago_bp.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    pago = Pago.get_by_id(id)
    if not pago:
        abort(404)
    pago.delete()
    return redirect(url_for('pago.index'))

@pago_bp.route("/recibo/<int:id>")
def recibo(id):
    pago = Pago.get_by_id(id)
    if not pago:
        abort(404)
    return pago_view.recibo(pago)
