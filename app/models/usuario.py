from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    perfil = db.Column(db.String(20), default='atendente')  # admin | atendente | coordenacao
    foto     = db.Column(db.String(200), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    ramal    = db.Column(db.String(10), nullable=True)
    cargo    = db.Column(db.String(100), nullable=True)
    ultimo_login = db.Column(db.DateTime, nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.perfil == 'admin'

    @property
    def is_coordenador(self):
        return self.perfil == 'coordenacao'

    @property
    def is_atendente(self):
        return self.perfil == 'atendente'

    def __repr__(self):
        return f'<Usuario {self.email} [{self.perfil}]>'
