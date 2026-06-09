# SIRAE – Sistema de Registro e Acompanhamento Estudantil

**Grupo 17 | Projeto Aplicado I – UniSENAI 2025/02**

## Descrição

Sistema web para cadastro e acompanhamento de ocorrências do setor de apoio estudantil, desenvolvido com Python, Flask e MySQL.

---

## Pré-requisitos

- Python 3.10 ou superior
- MySQL 8.0 ou superior
- pip

---

## Instalação e execução local

### 1. Clone o repositório

```bash
git clone https://github.com/Tayseeh/sirae-project.git
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

Edite `config.py` com suas credenciais MySQL:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://SEU_USUARIO:SUA_SENHA@localhost/sirae_db'
```

### 5. Crie as tabelas e popule com dados iniciais

```bash
python seed.py
```

### 6. Execute a aplicação

```bash
python run.py
```

Acesse: **http://localhost:5000**

---

## Credenciais de teste

| Usuário | Email | Senha | Perfil |
|---------|-------|-------|--------|
| Administrador | admin@sirae.com | admin123 | admin |
| Atendente | atendente@sirae.com | 123456 | atendente |
| Coordenadora | coord@sirae.com | 123456 | coordenacao |

---

## Dependências principais

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
mysql-connector-python==8.3.0
PyMySQL==1.2.0
Werkzeug==3.0.1
```

---

## Estrutura do projeto

```
sirae-project/
├── app/
│   ├── models/
│   │   ├── usuario.py       # Classe Usuario (POO)
│   │   └── ocorrencia.py    # Classes Ocorrencia e LogAuditoria (POO)
│   ├── routes/
│   │   ├── auth_routes.py   # Rotas de autenticação
│   │   └── main_routes.py   # Rotas principais (CRUD)
│   ├── templates/           # Páginas HTML (Jinja2)
│   ├── static/css/          # Estilos CSS
│   └── __init__.py          # Factory da aplicação
├── config.py                # Configurações do banco
├── run.py                   # Ponto de entrada
└── seed.py                  # Dados iniciais
```

---

## Estratégia de versionamento

O projeto adota o modelo **Git Flow simplificado** com uso de branches por funcionalidade. A branch `main` contém sempre a versão estável e funcional do sistema. Cada integrante trabalha em sua própria branch (`feature/nome-funcionalidade`) e abre um Pull Request para revisão antes de integrar ao `main`. Essa abordagem evita conflitos de código e garante que nenhuma alteração incompleta seja enviada para a versão principal.

Os commits seguem uma convenção descritiva: `feat:`, `fix:`, `docs:`, `refactor:`, indicando claramente o tipo de mudança. O histórico de commits comprova a participação de cada membro nas respectivas áreas de responsabilidade. O arquivo `.gitignore` foi configurado para excluir o ambiente virtual (`.venv/`), arquivos de configuração sensíveis e caches Python, garantindo que apenas o código-fonte e os arquivos essenciais sejam versionados. A integridade do código é mantida porque nenhuma alteração vai direto ao `main` sem revisão de ao menos um outro membro da equipe.
