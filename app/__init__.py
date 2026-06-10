from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Faça login para acessar esta página.'
login_manager.login_message_category = 'warning'


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # Sessão permanente para timeout funcionar
    @app.before_request
    def make_session_permanent():
        from flask import session
        session.permanent = True

    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import main_bp
    from app.routes.aluno_routes import aluno_bp
    from app.routes.admin_routes import admin_bp
    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.context_processor
    def inject_globals():
        return {'now': datetime.utcnow()}

    # Páginas de erro customizadas
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(admin_bp)

    return app
