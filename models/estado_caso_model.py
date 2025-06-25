from database import db 


class EstadoCaso(db.Model):
    __tablename__ = "estado_caso"
    id_estado_caso = db.Column(db.Integer,primary_key = True)
    estado_caso = db.Column(db.String(50), nullable = False)

    casos = db.relationship("Caso", back_populates="estado_caso")
    
    def __init__(self,estado_caso):
        self.estado_caso = estado_caso
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        

    @staticmethod
    def get_all():
        return EstadoCaso.query.all()
    

    @staticmethod
    def get_by_id(id_estado_caso):
        return EstadoCaso.query.get(id_estado_caso)

    def update(self, estado_caso=None):
        if estado_caso is not None:
            self.estado_caso = estado_caso
            db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()