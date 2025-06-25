from sqlalchemy import Column, Integer, Text, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import db

class Seguimiento(db.Model):
    __tablename__ = 'seguimiento'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_caso = Column(Integer, ForeignKey('caso.id_caso'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=False)
    archivo_url = Column(String(255))
    proximo_plazo = Column(Date)

    caso = db.relationship("Caso", back_populates="seguimientos")
    usuario = db.relationship("Usuario", back_populates="seguimientos")

    def __init__(self, id_caso, id_usuario, fecha, descripcion, archivo_url=None, proximo_plazo=None):
        self.id_caso = id_caso
        self.id_usuario = id_usuario
        self.fecha = fecha
        self.descripcion = descripcion
        self.archivo_url = archivo_url
        self.proximo_plazo = proximo_plazo

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Seguimiento.query.all()

    @staticmethod
    def get_by_id(id):
        return Seguimiento.query.get(id)

    def update(self, id_caso=None, id_usuario=None, fecha=None, descripcion=None, archivo_url=None, proximo_plazo=None):
        if id_caso is not None:
            self.id_caso = id_caso
        if id_usuario is not None:
            self.id_usuario = id_usuario
        if fecha is not None:
            self.fecha = fecha
        if descripcion is not None:
            self.descripcion = descripcion
        if archivo_url is not None:
            self.archivo_url = archivo_url
        if proximo_plazo is not None:
            self.proximo_plazo = proximo_plazo
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()