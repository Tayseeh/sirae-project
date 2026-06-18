from datetime import timedelta


class Config:
    SECRET_KEY = 'sirae-dev-only-change-in-production'

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://SEU_USUARIO:SUA_SENHA@localhost/sirae_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_PERMANENT = True
