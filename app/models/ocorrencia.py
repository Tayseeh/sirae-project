from app import db
from datetime import datetime


class Ocorrencia(db.Model):
    __tablename__ = 'ocorrencias'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    anexo_arquivo = db.Column(db.String(200), nullable=True)

    # status: aberta | em_acompanhamento | encerrada
    status = db.Column(db.String(20), default='aberta')

    # Quem criou (nunca muda)
    criado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Quem está responsável no momento (muda a cada encaminhamento)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_encerramento = db.Column(db.DateTime, nullable=True)

    # Relacionamentos
    criado_por  = db.relationship('Usuario', foreign_keys=[criado_por_id], backref='ocorrencias_criadas')
    responsavel = db.relationship('Usuario', foreign_keys=[responsavel_id], backref='ocorrencias_responsavel')
    logs = db.relationship('LogAuditoria', backref='ocorrencia', lazy=True,
                           order_by='LogAuditoria.data_hora')

    def encerrar(self):
        self.status = 'encerrada'
        self.data_encerramento = datetime.utcnow()

    def __repr__(self):
        return f'<Ocorrencia {self.id}>'


class LogAuditoria(db.Model):
    __tablename__ = 'logs_auditoria'

    id = db.Column(db.Integer, primary_key=True)
    ocorrencia_id = db.Column(db.Integer, db.ForeignKey('ocorrencias.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    acao = db.Column(db.String(50), nullable=False)
    descricao_acao = db.Column(db.Text, nullable=True)
    sigiloso       = db.Column(db.Boolean, default=False)  # visível só para coordenação
    anexo_log      = db.Column(db.String(200), nullable=True)  # anexo específico deste log
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref='logs')

    def __repr__(self):
        return f'<Log {self.acao} Ocorrencia#{self.ocorrencia_id}>'
