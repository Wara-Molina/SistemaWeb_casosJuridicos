from flask import render_template

def list(seguimientos):
    return render_template("seguimientos/index.html", seguimientos=seguimientos)

def create(casos=None, usuarios=None):
    return render_template("seguimientos/create.html", casos=casos, usuarios=usuarios)

def edit(seguimiento, casos=None, usuarios=None):
    return render_template("seguimientos/edit.html", seguimiento=seguimiento, casos=casos, usuarios=usuarios)