from flask import render_template

def list(casos):
    return render_template("casos/index.html", casos=casos)

def create(clientes, usuarios, tipos_caso, estados_caso, estados_pago):
    return render_template(
        "casos/create.html",
        clientes=clientes,
        usuarios=usuarios,
        tipos_casos= tipos_caso,
        estados_caso=estados_caso,
        estados_pago=estados_pago
    )

def edit(caso, clientes, usuarios, tipos_caso, estados_caso, estados_pago):
    return render_template(
        "casos/edit.html",
        caso=caso,
        clientes=clientes,
        usuarios=usuarios,
        tipos_casos=tipos_caso,
        estados_caso=estados_caso,
        estados_pago=estados_pago
    )