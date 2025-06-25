from flask import render_template

def list(bitacoras):
    return render_template("bitacoras/index.html", bitacoras=bitacoras)

def create():
    return render_template("bitacoras/create.html")