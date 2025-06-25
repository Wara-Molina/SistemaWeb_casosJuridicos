from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import db

class Bitacora(db.Model):
    __tablename__ = 'bitacora'

    id_bitacora = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    accion = Column(Text, nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)

    usuario = db.relationship("Usuario", back_populates="bitacoras")
    bitacoras = db.relationship("Bitacora", back_populates="usuario")
    
    def __init__(self, id_usuario, accion, fecha):
        self.id_usuario = id_usuario
        self.accion = accion
        self.fecha =fecha 
        
    def save(self):
        db.session.add(self)
        db.session.commit()
      
    @staticmethod    
    def get_all():
        return Bitacora.query.all()
    
    @staticmethod 
    def get_by_id(id_bitacora):
        return Bitacora.query.get(id_bitacora)
    

    def update(self, id_usuario=None, accion=None, fecha=None):
        if id_usuario is not None:
            self.id_usuario = id_usuario
        if accion is not None:
            self.accion = accion
        if fecha is not None:
            self.fecha = fecha
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        