from database import db

class Especialidad(db.Model):
    __tablename__ = "especialidad"

    id_especialidad= db.Column(db.Integer, primary_key=True)
    nombre_especialidad = db.Column(db.String(100), nullable=False)
    
    usuarios = db.relationship("Usuario", back_populates="especialidad")
    tipos_caso = db.relationship("TipoCaso", back_populates="especialidad")


    def __init__(self, nombre_especialidad):
        self.nombre_especialidad = nombre_especialidad

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Especialidad.query.all()

    @staticmethod
    def get_by_id(id_especialidad):
        return Especialidad.query.get(id_especialidad)

    def update(self, nombre_especialidad=None):
        if nombre_especialidad is not None:
            self.nombre_especialidad = nombre_especialidad
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
