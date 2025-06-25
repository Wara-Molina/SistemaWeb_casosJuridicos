# auth/user_login.py
from flask_login import UserMixin

class UserLogin(UserMixin):
    def __init__(self, usuario):
        self.usuario = usuario

    def get_id(self):
        return str(self.usuario.id_usuario)

    @property
    def id(self):
        return self.usuario.id_usuario  # <- esto soluciona el error actual

    @property
    def rol(self):
        return self.usuario.rol.nombre_rol

    @property
    def nombre(self):
        return self.usuario.nombre

    @property
    def username(self):
        return self.usuario.usuario
