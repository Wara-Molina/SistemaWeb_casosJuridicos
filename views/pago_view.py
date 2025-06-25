from flask import render_template

def list(pagos):
    return render_template("pagos/index.html", pagos=pagos)

def create(estados,casos, clientes):
    return render_template("pagos/create.html", estados=estados, casos=casos, clientes=clientes)

def edit(pago, estados,casos,clientes):
    return render_template("pagos/edit.html", pago=pago, estados=estados, casos=casos,clientes=clientes)

def recibo(pago):
    return render_template("pagos/recibo.html", pago=pago)