from database import db 
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id_usuario = db.Column(db.Integer,primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    usuario = db.Column(db.String(20), nullable = False, unique=True)
    password = db.Column (db.String, nullable=False)
    telefono = db.Column(db.String(20), nullable = True)
    direccion = db.Column(db.String(80), nullable = False)
    matricula = db.Column(db.String(50))
    id_especialidad = db.Column(db.Integer, db.ForeignKey('especialidad.id_especialidad'))
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id_rol'), nullable=False)
    id_estado_usuario = db.Column(db.Integer, db.ForeignKey('estado_usuario.id_estado_usuario'))
    activo = db.Column(db.Boolean, default=True, nullable=False)
    
  
    rol = db.relationship('Rol', back_populates='usuarios')
    estado_usuario = db.relationship('EstadoUsuario', back_populates='usuarios')
    especialidad = db.relationship('Especialidad', back_populates='usuarios')

    #bitacoras = db.relationship('Bitacora', back_populates='usuario')
    casos = db.relationship('Caso', back_populates='usuario')
   # notificaciones = db.relationship('Notificacion', back_populates='usuario')
    seguimientos = db.relationship('Seguimiento', back_populates='usuario')
    
    def __init__(self, nombre, usuario, password, telefono, direccion, matricula,
                 id_rol, id_estado_usuario, id_especialidad, activo=True):
        self.nombre = nombre
        self.usuario = usuario
        self.password=self.hash_password(password)
        self.telefono = telefono
        self.direccion = direccion
        self.matricula = matricula
        self.id_rol = id_rol
        self.id_estado_usuario = id_estado_usuario
        self.id_especialidad = id_especialidad
        self.activo = activo
    
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_all():
        return Usuario.query.all()

    @staticmethod
    def get_by_id(id_usuario):
        return Usuario.query.get(id_usuario)
    
    def update(self, nombre=None, usuario=None, password=None, telefono=None, direccion=None,
               matricula=None, id_rol=None, id_estado_usuario=None, id_especialidad=None, activo=None):
        if nombre is not None:
            self.nombre = nombre
        if usuario is not None:
            self.usuario = usuario
        if password is not None:
            self.password = self.hash_password(password)
        if telefono is not None:
            self.telefono = telefono
        if direccion is not None:
            self.direccion = direccion
        if matricula is not None:
            self.matricula = matricula
        if id_rol is not None:
            self.id_rol = id_rol
        if id_estado_usuario is not None:
            self.id_estado_usuario = id_estado_usuario
        if id_especialidad is not None:
            self.id_especialidad = id_especialidad
        if activo is not None:
            self.activo = bool(activo)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update_usuario(self, id_usuario):
        existing_user = Usuario.query.filter_by(usuario=id_usuario).first()
        if existing_user and existing_user.id != self.id:
            raise ValueError("El nombre de usuario ya está en uso.")
        self.usuario = id_usuario

    @staticmethod
    def get_activos():
        return Usuario.query.filter_by(activo=True).all()

    @staticmethod
    def get_inactivos():
        return Usuario.query.filter_by(activo=False).all()
    
   
    
    #@staticmethod
    #def get_by_usuario(username):
    #    return Usuario.query.filter_by(usuario=username).first()