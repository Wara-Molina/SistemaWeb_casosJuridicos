from sqlalchemy import Column, Integer, String, ForeignKey
from database import db

class TipoCaso(db.Model):
    __tablename__ = 'tipo_caso'

    id_tipo_caso = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(String(50), nullable=False)
    id_especialidad = Column(Integer, ForeignKey('especialidad.id_especialidad'))
   
    especialidad = db.relationship("Especialidad", back_populates="tipos_caso")
    casos = db.relationship("Caso", back_populates="tipo")

    def __init__(self, nombre_tipo, id_especialidad=None):
        self.nombre_tipo = nombre_tipo
        self.id_especialidad = id_especialidad

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return TipoCaso.query.all()

    @staticmethod
    def get_by_id(id_tipo_caso):
        return TipoCaso.query.get(id_tipo_caso)

    def update(self, nombre_tipo=None, id_especialidad=None):
        if nombre_tipo is not None:
            self.nombre_tipo = nombre_tipo
        if id_especialidad is not None:
            self.id_especialidad = id_especialidad
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()