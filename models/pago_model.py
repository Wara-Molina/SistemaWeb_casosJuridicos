from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DECIMAL
from database import db
from decimal import Decimal

class Pago(db.Model):
    __tablename__ = 'pago'

    id_pago= Column(Integer, primary_key=True, autoincrement=True)
    id_cliente= Column(Integer, ForeignKey('clientes.id'), nullable=False)
    id_caso = Column(Integer, ForeignKey('caso.id_caso'), nullable=False)
    fecha_pago = Column(Date, nullable=False)
    monto_pagado = Column(DECIMAL(10, 2), nullable=False)
    metodo_pago = Column(String(50),nullable=False)
    observaciones = Column(Text)
    id_estado_pago = Column(Integer, ForeignKey('estado_pago.id_estado_pago'))

    caso = db.relationship("Caso", back_populates="pagos")
    estado_pago = db.relationship("EstadoPago", back_populates="pagos")
    cliente = db.relationship("Cliente", backref="pagos")
    
    def __init__(self, id_cliente, id_caso, fecha_pago, monto_pagado, metodo_pago=None, observaciones=None, id_estado_pago=None):
        self.id_cliente = id_cliente
        self.id_caso = id_caso
        self.fecha_pago = fecha_pago
        self.monto_pagado = Decimal(str(monto_pagado))
        self.metodo_pago = metodo_pago
        self.observaciones = observaciones
        self.id_estado_pago = id_estado_pago

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Pago.query.all()

    @staticmethod
    def get_by_id(id_pago):
        return Pago.query.get(id_pago)

    def update(self,id_cliente=None, id_caso=None, fecha_pago=None, monto_pagado=None, metodo_pago=None, observaciones=None, id_estado_pago=None):
        if id_cliente is not None:
            self.id_cliente = id_cliente
        if id_caso is not None:
            self.id_caso = id_caso
        if fecha_pago is not None:
            self.fecha_pago = fecha_pago
        if monto_pagado is not None:
            self.monto_pagado = Decimal(str(monto_pagado))
        if metodo_pago is not None:
            self.metodo_pago = metodo_pago
        if observaciones is not None:
            self.observaciones = observaciones
        if id_estado_pago is not None:
            self.id_estado_pago = id_estado_pago
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
       
    def __repr__(self):
        return f"<Pago id={self.id_pago} monto={self.monto_pagado} caso={self.id_caso}>"