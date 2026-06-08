from app import create_app, db
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from app.models.ocorrencia import Ocorrencia, LogAuditoria

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Usuario': Usuario, 'Aluno': Aluno,
            'Ocorrencia': Ocorrencia, 'LogAuditoria': LogAuditoria}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
