from flask import render_template

def list(audiencias, id_caso=None):
    return render_template("audiencias/index.html", audiencias=audiencias, id_caso=id_caso)

def create(id_caso, estados):
    return render_template("audiencias/create_sin_caso.html", id_caso=id_caso, estados=estados)

def create_general(casos, estados):
    return render_template("audiencias/create_general.html", casos=casos, estados=estados)

def edit(audiencia, estados):
    return render_template("audiencias/edit.html", audiencia=audiencia, estados=estados)