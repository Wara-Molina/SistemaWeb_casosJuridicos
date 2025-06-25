from database import db

class EstadoAudiencia(db.Model):
    __tablename__ = "estado_audiencia"

    id_estado_audiencia= db.Column(db.Integer, primary_key=True)
    nombre_estado_audiencia = db.Column(db.String(100), nullable=False)

    # Relación con Audiencia
    audiencias = db.relationship('Audiencia', back_populates='estado_audiencia')

    def __init__(self, nombre_estado_audiencia):
        self.nombre_estado_audiencia = nombre_estado_audiencia

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return EstadoAudiencia.query.all()

    @staticmethod
    def get_by_id(id_estado_audiencia):
        return EstadoAudiencia.query.get(id_estado_audiencia)

    def update(self, nombre_estado_audiencia=None):
        if nombre_estado_audiencia is not None:
            self.nombre_estado_audiencia = nombre_estado_audiencia
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
