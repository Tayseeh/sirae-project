from app import db
from datetime import datetime, timezone, timedelta

BRASILIA = timezone(timedelta(hours=-3))

class LogAluno(db.Model):
    __tablename__ = 'logs_aluno'

    id          = db.Column(db.Integer, primary_key=True)
    aluno_id    = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    usuario_id  = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    acao        = db.Column(db.String(50), nullable=False)   # editou, desativou, reativou
    descricao   = db.Column(db.Text, nullable=True)
    data_hora   = db.Column(db.DateTime, default=lambda: datetime.now(BRASILIA))

    aluno   = db.relationship('Aluno',   backref=db.backref('logs', lazy='dynamic', order_by='LogAluno.data_hora.desc()'))
    usuario = db.relationship('Usuario', backref=db.backref('logs_aluno', lazy=True))
