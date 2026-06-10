import os
from datetime import timedelta
 
# Carrega o .env antes de qualquer coisa (caso python-dotenv esteja instalado)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
 
 
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sirae-dev-only-change-in-production')
 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError(
            "DATABASE_URL não configurada. "
            "Defina a variável de ambiente DATABASE_URL com sua string de conexão MySQL. "
            "Exemplo: mysql+mysqlconnector://usuario:senha@localhost/sirae_db"
        )
 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_PERMANENT = True
 