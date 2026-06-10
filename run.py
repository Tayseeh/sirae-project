import os

# Carrega variáveis de ambiente do arquivo .env (desenvolvimento local).
# Em produção, defina as variáveis diretamente no ambiente do servidor.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv não instalado — use variáveis de ambiente do sistema

from app import create_app, db
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from app.models.ocorrencia import Ocorrencia, LogAuditoria
from app.models.log_admin import LogAdmin

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Usuario': Usuario, 'Aluno': Aluno,
            'Ocorrencia': Ocorrencia, 'LogAuditoria': LogAuditoria, 'LogAdmin': LogAdmin}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
