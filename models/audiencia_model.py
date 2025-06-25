from database import db

class Audiencia(db.Model):
    __tablename__ = "audiencia"

    id_audiencia = db.Column(db.Integer, primary_key=True)
    id_caso = db.Column(db.Integer, db.ForeignKey('caso.id_caso'), nullable=False)
    fecha_audiencia = db.Column(db.Date, nullable=False)
    hora_audiencia = db.Column(db.Time, nullable=False)
    lugar = db.Column(db.String(200), nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    id_estado_audiencia = db.Column(db.Integer, db.ForeignKey('estado_audiencia.id_estado_audiencia'), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

   
    estado_audiencia = db.relationship('EstadoAudiencia', back_populates='audiencias')
    caso = db.relationship('Caso', back_populates='audiencias') 

    def __init__(self, id_caso, fecha_audiencia, hora_audiencia, lugar, observaciones, id_estado_audiencia, activo=True):
        self.id_caso = id_caso
        self.fecha_audiencia = fecha_audiencia
        self.hora_audiencia = hora_audiencia
        self.lugar = lugar
        self.observaciones = observaciones
        self.id_estado_audiencia = id_estado_audiencia
        self.activo = activo

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Audiencia.query.all()

    @staticmethod
    def get_by_id(id_audiencia):
        return Audiencia.query.get(id_audiencia)
    
    @staticmethod
    def get_by_caso(id_caso):
        """PUNTO 2: Devuelve todas las audiencias de un caso específico."""
        return Audiencia.query.filter_by(id_caso=id_caso).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id_audiencia" and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def deactivate(self):
        """PUNTO 3: Elimina lógicamente (soft delete) una audiencia."""
        self.activo = False
        db.session.commit()