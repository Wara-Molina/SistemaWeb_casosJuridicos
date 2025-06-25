from database import db 


class Rol(db.Model):
    __tablename__ = "rol"
    id_rol = db.Column(db.Integer,primary_key = True)
    nombre_rol = db.Column(db.String(50), nullable = False)
    
    usuarios = db.relationship('Usuario', back_populates='rol')

    def __init__(self,nombre_rol):
        self.nombre_rol = nombre_rol
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Rol.query.all()
    

    @staticmethod
    def get_by_id(id_rol):
        return Rol.query.get(id_rol)

    def update(self, nombre_rol=None):
        if nombre_rol is not None:
            self.nombre_rol = nombre_rol
            db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
