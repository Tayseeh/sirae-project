import os
from datetime import timedelta


class Config:
    # Em produção, defina SECRET_KEY como variável de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sirae-senai-2026-chave-local')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqlconnector://root:admin123@localhost/sirae_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Sessão expira após 2 horas de inatividade
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_PERMANENT = True
