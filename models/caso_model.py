from database import db
from sqlalchemy import Numeric
from decimal import Decimal
class Caso(db.Model):
    __tablename__ = "caso"

    id_caso = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipo_caso.id_tipo_caso'), nullable=False) 
    id_estado_caso = db.Column(db.Integer, db.ForeignKey('estado_caso.id_estado_caso'), nullable=False)
    id_estado_pago = db.Column(db.Integer, db.ForeignKey('estado_pago.id_estado_pago'), nullable=False)

    fecha_apertura = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    monto_total = db.Column(Numeric(10, 2), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    # Relaciones
    cliente = db.relationship('Cliente', back_populates='casos')
    usuario = db.relationship('Usuario', back_populates='casos')
    tipo = db.relationship('TipoCaso', back_populates='casos')  
    estado_caso = db.relationship('EstadoCaso', back_populates='casos')
    estado_pago = db.relationship('EstadoPago', back_populates='casos')
    audiencias = db.relationship('Audiencia', back_populates='caso')
    pagos = db.relationship("Pago", back_populates="caso")
    seguimientos = db.relationship('Seguimiento', back_populates='caso')
    documentos = db.relationship('Documento', back_populates='caso')


    def __init__(self, id_cliente, id_usuario, id_tipo, id_estado_caso, fecha_apertura, descripcion, monto_total, id_estado_pago, activo=True):
        self.id_cliente = id_cliente
        self.id_usuario = id_usuario
        self.id_tipo = id_tipo
        self.id_estado_caso = id_estado_caso
        self.fecha_apertura = fecha_apertura
        self.descripcion = descripcion
        self.monto_total = monto_total
        self.id_estado_pago = id_estado_pago
        self.activo = activo

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Caso.query.all()

    @staticmethod
    def get_by_id(id_caso):
        return Caso.query.get(id_caso)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @property
    def total_pagado(self):
        return sum(p.monto_pagado for p in self.pagos)

    @property
    def saldo_restante(self):
    # Aseguramos que monto_total es Decimal (de Numeric)
        monto_total = self.monto_total if isinstance(self.monto_total, Decimal) else Decimal(str(self.monto_total))
        total_pagado = self.total_pagado if isinstance(self.total_pagado, Decimal) else Decimal(str(self.total_pagado))
        return monto_total - total_pagado

    def __repr__(self):
        return f"<Caso id={self.id} titulo={self.titulo} total={self.monto_total}>"