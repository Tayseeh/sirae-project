from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializa as extensões
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Liga as extensões ao app
    db.init_app(app)
    login_manager.init_app(app)

    # Importa e registra as rotas (Blueprints)
    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import main_bp
    
    # Importar modelos para o user_loader
    from app.models.usuario import Usuario
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app