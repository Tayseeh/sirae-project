from app import db
from datetime import datetime

class Ocorrencia(db.Model):
    __tablename__ = 'ocorrencias'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    anexo_arquivo = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default='aberta')  # aberta, encerrada
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_encerramento = db.Column(db.DateTime, nullable=True)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    def encerrar(self):
        """Método para encerrar a ocorrência (RF04)"""
        self.status = 'encerrada'
        self.data_encerramento = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Ocorrencia {self.id} - {self.aluno_nome}>'