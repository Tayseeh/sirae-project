# SIRAE – Sistema de Registro e Acompanhamento Estudantil

**Projeto Aplicado I

---

## Sobre o projeto

O SIRAE é uma aplicação web desenvolvida para o setor de apoio estudantil da Faculdade de Tecnologia SENAI Antônio Adolpho Lobbe. O sistema centraliza o registro, acompanhamento e encerramento de ocorrências envolvendo alunos dos cursos técnicos, de graduação e pós-graduação, substituindo o controle manual em planilhas ou documentos avulsos.

---

## Pré-requisitos

- Python 3.10 ou superior
- MySQL 8.0 ou superior
- pip

---

## Instalação e execução local

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/sirae-project.git
cd sirae-project
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

No MySQL, crie o banco:

```sql
CREATE DATABASE sirae_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Edite o arquivo `config.py` com suas credenciais:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://SEU_USUARIO:SUA_SENHA@localhost/sirae_db'
```

### 5. Crie as tabelas e popule os dados iniciais

```bash
python seed.py
```

### 6. Inicie a aplicação

```bash
python run.py
```

Acesse em: **http://localhost:5000**

---

## Credenciais de teste

| Perfil | E-mail | Senha |
|--------|--------|-------|
| Administrador (TI) | admin@sirae.com.br | admin123 |
| Atendente | ana.lima@sirae.com.br | 123456 |
| Atendente | carlos.m@sirae.com.br | 123456 |
| Atendente | patricia@sirae.com.br | 123456 |
| Pedagogo | fernanda.p@sirae.com.br | 123456 |
| Pedagogo | rodrigo.b@sirae.com.br | 123456 |
| Coordenação | marcos.r@sirae.com.br | 123456 |
| Coordenação | juliana.c@sirae.com.br | 123456 |

---

## Estrutura do projeto

```
sirae-project/
├── app/
│   ├── models/
│   │   ├── usuario.py          # Entidade Usuario
│   │   ├── aluno.py            # Entidade Aluno
│   │   ├── ocorrencia.py       # Entidades Ocorrencia e LogAuditoria
│   │   └── log_admin.py        # Entidade LogAdmin
│   ├── routes/
│   │   ├── auth_routes.py      # Autenticação e perfil do usuário
│   │   ├── main_routes.py      # Ocorrências, dashboard e relatórios
│   │   ├── aluno_routes.py     # CRUD de alunos
│   │   └── admin_routes.py     # Gestão de usuários (perfil admin)
│   ├── templates/              # Templates HTML com Jinja2
│   ├── static/
│   │   └── css/style.css       # Design system do SIRAE
│   └── __init__.py             # Factory da aplicação Flask
├── config.py                   # Configurações e variáveis de ambiente
├── run.py                      # Ponto de entrada da aplicação
└── seed.py                     # Carga inicial de dados para teste
```

---

## Dependências principais

```
Flask
Flask-SQLAlchemy
Flask-Login
mysql-connector-python
Werkzeug
```

---

## Estratégia de versionamento

O projeto utiliza Git com o modelo de branches por funcionalidade. A branch `main` mantém sempre a versão estável do sistema. O desenvolvimento de novas funcionalidades ocorre em branches separadas, que passam por revisão antes de serem integradas à principal.

Os commits seguem a convenção `feat:`, `fix:`, `docs:` e `refactor:`, tornando o histórico legível e rastreável. O arquivo `.gitignore` exclui o ambiente virtual, caches e arquivos de configuração sensíveis, garantindo que apenas o código-fonte seja versionado. Nenhuma alteração é enviada diretamente ao `main` sem validação prévia, o que protege a integridade da versão de produção.
