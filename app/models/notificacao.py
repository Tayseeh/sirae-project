from app import db
from datetime import datetime, timezone, timedelta

BRASILIA = timezone(timedelta(hours=-3))


class Notificacao(db.Model):
    """Notificações geradas quando uma ocorrência é encaminhada para um usuário."""
    __tablename__ = 'notificacoes'

    id             = db.Column(db.Integer, primary_key=True)
    usuario_id     = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    ocorrencia_id  = db.Column(db.Integer, db.ForeignKey('ocorrencias.id'), nullable=False)
    mensagem       = db.Column(db.String(200), nullable=False)
    lida           = db.Column(db.Boolean, default=False)
    data_hora      = db.Column(db.DateTime, default=lambda: datetime.now(BRASILIA))

    usuario    = db.relationship('Usuario', backref='notificacoes')
    ocorrencia = db.relationship('Ocorrencia', backref='notificacoes')

    def __repr__(self):
        return f'<Notificacao user={self.usuario_id} occ={self.ocorrencia_id} lida={self.lida}>'
