from flask import render_template

def list(documentos):
    return render_template("documentos/index.html", documentos=documentos)

def create(casos):
    return render_template("documentos/create.html", casos=casos)

def edit(documento, casos):
    return render_template("documentos/edit.html", documento=documento, casos=casos)