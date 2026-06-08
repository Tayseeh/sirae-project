from app import db
from datetime import datetime
import re


def limpar_numeros(valor):
    """Remove tudo que não é número"""
    return re.sub(r'\D', '', valor or '')



def formatar_cpf(cpf):
    nums = limpar_numeros(cpf)
    if len(nums) == 11:
        return f'{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}'
    return cpf


def formatar_telefone(tel):
    nums = limpar_numeros(tel)
    if len(nums) == 11:  # celular com DDD
        return f'({nums[:2]}) {nums[2:7]}-{nums[7:]}'
    if len(nums) == 10:  # fixo com DDD
        return f'({nums[:2]}) {nums[2:6]}-{nums[6:]}'
    return tel


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)

    # Foto
    foto = db.Column(db.String(200), nullable=True)  # caminho relativo em static/uploads/fotos/

    # Dados pessoais
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    cpf = db.Column(db.String(14), unique=True, nullable=True)   # 000.000.000-00
    email = db.Column(db.String(100), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)           # (48) 99999-9999

    # Dados acadêmicos
    matricula = db.Column(db.String(20), unique=True, nullable=True)
    nivel = db.Column(db.String(30), nullable=True)              # fundamental, medio
    serie = db.Column(db.String(30), nullable=True)              # 6º ano, 1º ano EM...
    turma = db.Column(db.String(10), nullable=True)              # A, B, C...
    turno = db.Column(db.String(10), nullable=True)              # manhã, tarde, noite

    # Responsável (obrigatório para menores)
    responsavel_nome = db.Column(db.String(100), nullable=True)
    responsavel_parentesco = db.Column(db.String(30), nullable=True)
    responsavel_cpf = db.Column(db.String(14), nullable=True)
    responsavel_contato = db.Column(db.String(20), nullable=True)
    responsavel_email = db.Column(db.String(100), nullable=True)

    # Controle
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento
    ocorrencias = db.relationship('Ocorrencia', backref='aluno', lazy=True)

    @property
    def idade(self):
        if not self.data_nascimento:
            return None
        hoje = datetime.today().date()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def menor_de_idade(self):
        return self.idade is not None and self.idade < 18

    @property
    def serie_completa(self):
        """Ex: '6º ano EF · Turma A · manhã'"""
        partes = []
        if self.serie:
            partes.append(self.serie)
        if self.turma:
            partes.append(f'Turma {self.turma}')
        if self.turno:
            partes.append(self.turno)
        return ' · '.join(partes) if partes else '—'

    @property
    def total_ocorrencias(self):
        return len(self.ocorrencias)

    @property
    def ocorrencias_ativas(self):
        return [o for o in self.ocorrencias if o.status != 'encerrada']

    def __repr__(self):
        return f'<Aluno {self.nome}>'
