from database import db

class Notificacion(db.Model):
    __tablename__ = "notificacion"

    id_notificacion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    mensaje = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    leido = db.Column(db.Boolean, default=False)

    # Relación con Usuario
    usuario = db.relationship('Usuario', back_populates='notificaciones')

    def __init__(self, id_usuario, mensaje, fecha, leido=False):
        self.id_usuario = id_usuario
        self.mensaje = mensaje
        self.fecha = fecha
        self.leido = leido

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Notificacion.query.all()

    @staticmethod
    def get_by_id(id_notificacion):
        return Notificacion.query.get(id_notificacion)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
