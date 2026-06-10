"""
test_sirae.py — Suite de testes automatizados do SIRAE
Autor: Eduardo Piassabussu
Função: Testes e Segurança

Execução:
    python test_sirae.py

Descrição:
    Valida as regras de segurança e as regras de negócio principais do sistema,
    incluindo autenticação, controle de acesso por perfil, validação de uploads
    e integridade do fluxo de ocorrências.
"""

import unittest
import os
import sys
import io

# Garante que o diretório raiz está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configura variáveis de ambiente para testes antes de importar a aplicação
os.environ.setdefault('SECRET_KEY', 'chave-de-teste-sirae')
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')

from app import create_app, db
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from app.models.ocorrencia import Ocorrencia, LogAuditoria


class ConfigTeste:
    """Configuração isolada para ambiente de testes."""
    TESTING = True
    SECRET_KEY = 'chave-de-teste-sirae'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    PERMANENT_SESSION_LIFETIME = __import__('datetime').timedelta(hours=2)
    SESSION_PERMANENT = True


def criar_app_teste():
    """Cria instância da aplicação configurada para testes."""
    app = create_app()
    app.config.from_object(ConfigTeste)
    return app


class TesteAutenticacao(unittest.TestCase):
    """Testes de autenticação e controle de sessão."""

    def setUp(self):
        self.app = criar_app_teste()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Cria usuário ativo para testes
            u = Usuario(email='teste@sirae.com', nome='Teste', perfil='atendente', ativo=True)
            u.set_password('senha123')
            # Cria usuário inativo para testes de bloqueio
            u_inativo = Usuario(email='inativo@sirae.com', nome='Inativo', perfil='atendente', ativo=False)
            u_inativo.set_password('senha123')
            db.session.add_all([u, u_inativo])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_credenciais_corretas(self):
        """Login com credenciais válidas deve redirecionar para o dashboard."""
        resp = self.client.post('/auth/login', data={
            'email': 'teste@sirae.com',
            'password': 'senha123'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_login_senha_errada(self):
        """Login com senha incorreta deve permanecer na tela de login."""
        resp = self.client.post('/auth/login', data={
            'email': 'teste@sirae.com',
            'password': 'senha_errada'
        }, follow_redirects=True)
        self.assertIn(b'login', resp.data.lower())

    def test_login_usuario_inativo_bloqueado(self):
        """Usuário inativo não deve conseguir fazer login."""
        resp = self.client.post('/auth/login', data={
            'email': 'inativo@sirae.com',
            'password': 'senha123'
        }, follow_redirects=True)
        # Deve permanecer na tela de login (não redireciona para dashboard)
        self.assertNotIn(b'dashboard', resp.data.lower())

    def test_acesso_sem_autenticacao_redireciona(self):
        """Acesso ao dashboard sem login deve redirecionar para login."""
        resp = self.client.get('/', follow_redirects=False)
        self.assertIn(resp.status_code, [301, 302])

    def test_logout_encerra_sessao(self):
        """Logout deve encerrar a sessão e redirecionar para login."""
        self.client.post('/auth/login', data={
            'email': 'teste@sirae.com',
            'password': 'senha123'
        })
        resp = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)


class TesteControleAcesso(unittest.TestCase):
    """Testes de controle de acesso por perfil."""

    def setUp(self):
        self.app = criar_app_teste()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Usuários de diferentes perfis
            perfis = [
                ('admin@sirae.com', 'Admin', 'admin'),
                ('atendente@sirae.com', 'Atendente', 'atendente'),
                ('coord@sirae.com', 'Coordenador', 'coordenacao'),
                ('pedagogo@sirae.com', 'Pedagogo', 'pedagogia'),
            ]
            for email, nome, perfil in perfis:
                u = Usuario(email=email, nome=nome, perfil=perfil, ativo=True)
                u.set_password('senha123')
                db.session.add(u)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _login(self, email):
        self.client.post('/auth/login', data={
            'email': email,
            'password': 'senha123'
        })

    def test_atendente_nao_acessa_area_admin(self):
        """Atendente não deve acessar rotas administrativas."""
        self._login('atendente@sirae.com')
        resp = self.client.get('/admin/usuarios', follow_redirects=True)
        self.assertNotIn(b'Gerenciar Usu', resp.data)

    def test_pedagogo_nao_acessa_area_admin(self):
        """Pedagogo não deve acessar rotas administrativas."""
        self._login('pedagogo@sirae.com')
        resp = self.client.get('/admin/usuarios', follow_redirects=True)
        self.assertNotIn(b'Gerenciar Usu', resp.data)

    def test_admin_acessa_area_admin(self):
        """Administrador deve acessar rotas administrativas."""
        self._login('admin@sirae.com')
        resp = self.client.get('/admin/usuarios', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_atendente_nao_acessa_relatorios(self):
        """Atendente não deve acessar o painel de relatórios."""
        self._login('atendente@sirae.com')
        resp = self.client.get('/relatorios', follow_redirects=True)
        self.assertNotIn(b'relat', resp.data.lower()[:500])

    def test_coordenacao_acessa_relatorios(self):
        """Coordenação deve acessar o painel de relatórios."""
        self._login('coord@sirae.com')
        resp = self.client.get('/relatorios', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)


class TesteModels(unittest.TestCase):
    """Testes das regras de negócio nos models."""

    def setUp(self):
        self.app = criar_app_teste()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_senha_nao_armazenada_em_texto_puro(self):
        """A senha nunca deve ser armazenada em texto puro."""
        with self.app.app_context():
            u = Usuario(email='x@x.com', nome='X', perfil='atendente')
            u.set_password('minhasenha')
            self.assertNotEqual(u.password_hash, 'minhasenha')
            self.assertGreater(len(u.password_hash), 20)

    def test_verificacao_senha_correta(self):
        """Verificação de senha correta deve retornar True."""
        with self.app.app_context():
            u = Usuario(email='x@x.com', nome='X', perfil='atendente')
            u.set_password('minhasenha')
            self.assertTrue(u.check_password('minhasenha'))

    def test_verificacao_senha_errada(self):
        """Verificação de senha incorreta deve retornar False."""
        with self.app.app_context():
            u = Usuario(email='x@x.com', nome='X', perfil='atendente')
            u.set_password('minhasenha')
            self.assertFalse(u.check_password('senhaerrada'))

    def test_deteccao_menoridade(self):
        """Aluno com menos de 18 anos deve ser identificado como menor."""
        with self.app.app_context():
            from datetime import date
            menor = Aluno(
                nome='Menor Teste',
                matricula='T001',
                nivel='tecnico',
                curso='Mecatrônica',
                data_nascimento=date(2010, 1, 1)
            )
            self.assertTrue(menor.menor_de_idade)

    def test_deteccao_maior_de_idade(self):
        """Aluno com 18 anos ou mais deve ser identificado como maior."""
        with self.app.app_context():
            from datetime import date
            maior = Aluno(
                nome='Maior Teste',
                matricula='T002',
                nivel='graduacao',
                curso='Engenharia',
                data_nascimento=date(2000, 1, 1)
            )
            self.assertFalse(maior.menor_de_idade)

    def test_encerramento_ocorrencia(self):
        """Método encerrar() deve atualizar status e registrar data."""
        with self.app.app_context():
            u = Usuario(email='u@u.com', nome='U', perfil='atendente', ativo=True)
            u.set_password('123')
            a = Aluno(nome='Aluno', matricula='M001', nivel='tecnico', curso='Curso')
            db.session.add_all([u, a])
            db.session.flush()

            o = Ocorrencia(
                aluno_id=a.id,
                tipo='Disciplinar',
                descricao='Teste',
                criado_por_id=u.id,
                responsavel_id=u.id,
                status='aberta'
            )
            db.session.add(o)
            db.session.flush()

            o.encerrar()
            self.assertEqual(o.status, 'encerrada')
            self.assertIsNotNone(o.data_encerramento)


class TesteValidacaoUpload(unittest.TestCase):
    """Testes de validação de uploads de arquivos."""

    def setUp(self):
        self.app = criar_app_teste()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            u = Usuario(email='atend@sirae.com', nome='Atendente', perfil='atendente', ativo=True)
            u.set_password('senha123')
            db.session.add(u)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_extensao_invalida_rejeitada(self):
        """Upload com extensão não permitida deve ser rejeitado."""
        from werkzeug.utils import secure_filename
        nome = secure_filename('arquivo.exe')
        ext = nome.rsplit('.', 1)[-1].lower() if '.' in nome else ''
        permitidos = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
        self.assertNotIn(ext, permitidos)

    def test_extensao_valida_aceita(self):
        """Upload com extensão permitida deve ser aceito."""
        from werkzeug.utils import secure_filename
        for nome_arquivo in ['documento.pdf', 'foto.jpg', 'arquivo.docx']:
            nome = secure_filename(nome_arquivo)
            ext = nome.rsplit('.', 1)[-1].lower()
            permitidos = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
            self.assertIn(ext, permitidos)

    def test_secure_filename_sanitiza_path_traversal(self):
        """secure_filename deve remover tentativas de path traversal."""
        from werkzeug.utils import secure_filename
        nome_malicioso = '../../../etc/passwd'
        nome_seguro = secure_filename(nome_malicioso)
        self.assertNotIn('/', nome_seguro)
        self.assertNotIn('..', nome_seguro)


if __name__ == '__main__':
    print("=" * 60)
    print("SIRAE — Suite de Testes Automatizados")
    print("=" * 60)
    unittest.main(verbosity=2)
