from app import db
from datetime import datetime, timezone


class LogAdmin(db.Model):
    """Log de ações administrativas feitas pela TI"""
    __tablename__ = 'logs_admin'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    acao = db.Column(db.String(50), nullable=False)   # criou_usuario, editou_usuario, desativou_usuario
    alvo_nome = db.Column(db.String(100), nullable=True)  # nome do usuário afetado
    descricao = db.Column(db.Text, nullable=True)
    data_hora = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = db.relationship('Usuario', backref='logs_admin')

    def __repr__(self):
        return f'<LogAdmin {self.acao} por {self.usuario_id}>'
