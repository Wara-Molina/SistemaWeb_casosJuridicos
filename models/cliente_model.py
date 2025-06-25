from database import db 


class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer,primary_key = True)
    nombre = db.Column(db.String(50), nullable = False)
    cedula = db.Column(db.String(50), nullable = False)
    direccion = db.Column(db.String(50), nullable = False)
    telefono = db.Column(db.String(20),nullable = False)
    email = db.Column(db.String(100),nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    
    casos = db.relationship("Caso", back_populates="cliente")

    def __init__(self,nombre,cedula,direccion,telefono,email,activo= True):
        self.nombre = nombre
        self.cedula = cedula
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.activo = activo
    

    def save(self):
        db.session.add(self)
        db.session.commit()
        

    @staticmethod
    def get_all():
        return Cliente.query.all()
    

    @staticmethod
    def get_by_id(id):
        return Cliente.query.get(id)

    def update(self, nombre= None,cedula= None,direccion= None,telefono= None,email= None,activo= None):
        if nombre is not None:
            self.nombre = nombre
        if cedula is not None:
            self.cedula = cedula
        if direccion is not None:
            self.direccion = direccion
        if telefono is not None:
            self.telefono = telefono
        if email is not None:
            self.email = email
        if activo is not None:
            self.activo = bool(activo)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()