
from database import db
from datetime import datetime

class Documento(db.Model):
    __tablename__ = "documento"

    id_documento = db.Column(db.Integer, primary_key=True)
    id_caso = db.Column(db.Integer, db.ForeignKey('caso.id_caso'), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    archivo_path = db.Column(db.String(255), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    # Relación con Caso
    caso = db.relationship('Caso', back_populates='documentos')

    def __init__(self, id_caso, titulo, descripcion, archivo_path, fecha_subida, activo=True):
        self.id_caso = id_caso
        self.titulo = titulo
        self.descripcion = descripcion
        self.archivo_path = archivo_path
        self.fecha_subida = fecha_subida
        self.activo = activo

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Documento.query.all()

    @staticmethod
    def get_by_id(id_documento):
        return Documento.query.get(id_documento)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
