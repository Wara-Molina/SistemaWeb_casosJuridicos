from database import db 


class EstadoUsuario(db.Model):
    __tablename__ = "estado_usuario"
    id_estado_usuario = db.Column(db.Integer,primary_key = True)
    nombre_estado = db.Column(db.String(20), nullable = False)
    
    usuarios = db.relationship('Usuario', back_populates='estado_usuario')

    def __init__(self,nombre_estado):
        self.nombre_estado = nombre_estado
    

    def save(self):
        db.session.add(self)
        db.session.commit()
        

    @staticmethod
    def get_all():
        return EstadoUsuario.query.all()
    

    @staticmethod
    def get_by_id(id_estado_usuario):
        return EstadoUsuario.query.get(id_estado_usuario)

    def update(self, estado=None):
        if estado is not None:
            self.estado = estado
            db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()