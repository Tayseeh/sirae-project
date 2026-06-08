import os

class Config:
    SECRET_KEY = 'chave-secreta-sirae-av5'
    # CORRIJA ESTA LINHA - adicione "localhost/"
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:admin123@localhost/sirae_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False