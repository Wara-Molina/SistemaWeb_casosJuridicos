from flask import render_template

def list(usuarios):
    return render_template("usuarios/index.html", usuarios=usuarios)

def create(roles, estado_usuarios, especialidades):
    return render_template(
        "usuarios/create.html",
        roles=roles,
        estado_usuarios=estado_usuarios,
        especialidades=especialidades
    )


def edit(usuario, roles, estado_usuarios, especialidades):
    return render_template(
        "usuarios/edit.html",
        usuario=usuario,
        roles=roles,
        estado_usuarios=estado_usuarios,
        especialidades=especialidades
    )