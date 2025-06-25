from flask import render_template

def list(notificaciones):
    return render_template("notificaciones/index.html", notificaciones=notificaciones)

def create():
    return render_template("notificaciones/create.html")

def edit(notificacion):
    return render_template("notificaciones/edit.html", notificacion=notificacion)