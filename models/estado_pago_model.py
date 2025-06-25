from database import db 


class EstadoPago(db.Model):
    __tablename__ = "estado_pago"
    id_estado_pago = db.Column(db.Integer,primary_key = True)
    estado = db.Column(db.String(50), nullable = False)
    
    casos = db.relationship("Caso", back_populates="estado_pago")
    pagos = db.relationship("Pago", back_populates="estado_pago")

    def __init__(self,estado):
        self.estado = estado
    

    def save(self):
        db.session.add(self)
        db.session.commit()
        

    @staticmethod
    def get_all():
        return EstadoPago.query.all()
    

    @staticmethod
    def get_by_id(id_estado_pago):
        return EstadoPago.query.get(id_estado_pago)

    def update(self, estado=None):
        if estado is not None:
            self.estado = estado
            db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()