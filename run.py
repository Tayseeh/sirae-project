from app import create_app, db
from app.models.usuario import Usuario
from app.models.ocorrencia import Ocorrencia

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Usuario': Usuario, 'Ocorrencia': Ocorrencia}

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Cria as tabelas automaticamente
    app.run(debug=True)