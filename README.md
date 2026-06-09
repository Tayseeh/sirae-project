# SIRAE — Sistema de Registro e Acompanhamento Estudantil

> Desenvolvido para o **SENAI Antônio Adolpho Lobbe** · São Carlos, SP  
> Disciplina: Projeto Aplicado I · UniSENAI  

---

## Sobre o projeto

O SIRAE é uma aplicação web de gestão de ocorrências estudantis desenvolvida para o setor de apoio do SENAI AAL. Permite o registro, acompanhamento e encerramento de ocorrências de alunos dos cursos técnicos, de graduação e pós-graduação, com controle de acesso por perfil (Atendente, Pedagogo, Coordenação e Administrador TI).

---

## Pré-requisitos

- Python 3.10 ou superior
- MySQL 8.0 ou superior
- pip (gerenciador de pacotes Python)

---

## Subir no GitHub (primeira vez)

> Execute os comandos no terminal integrado do VS Code (`Ctrl+\`` ou Terminal → Novo Terminal)

### 1. Crie o `.gitignore` na raiz do projeto

```bash
echo ".venv/
__pycache__/
*.pyc
app/static/uploads/
*.db
.env" > .gitignore
```

### 2. Inicialize o repositório Git

```bash
git init
git add .
git commit -m "feat: SIRAE - Sistema de Registro e Acompanhamento Estudantil"
```

### 3. Crie o repositório no GitHub

- Acesse [github.com](https://github.com) → botão **New repository**
- Nome: `sirae-project` · Visibilidade: **Public**
- **Não** marque nenhuma opção de inicialização (README, .gitignore)
- Clique em **Create repository**

### 4. Conecte e envie

```bash
git remote add origin https://github.com/SEU-USUARIO/sirae-project.git
git branch -M main
git push -u origin main
```

### 5. Para enviar atualizações futuras

```bash
git add .
git commit -m "descricao da alteracao"
git push
```

---

## Instalação e execução local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/sirae-project.git
cd sirae-project
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Crie o banco no MySQL:

```sql
CREATE DATABASE sirae_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Configure as variáveis de ambiente (ou edite `config.py`):

```bash
# Windows (PowerShell)
$env:DATABASE_URL = "mysql+mysqlconnector://root:SUA_SENHA@localhost/sirae_db"
$env:SECRET_KEY   = "chave-secreta-desenvolvimento"

# Linux / macOS
export DATABASE_URL="mysql+mysqlconnector://root:SUA_SENHA@localhost/sirae_db"
export SECRET_KEY="chave-secreta-desenvolvimento"
```

### 5. Crie as tabelas e popule o banco

```bash
python run.py        # cria as tabelas automaticamente
# Em outro terminal (ou após Ctrl+C):
python seed.py       # insere dados de exemplo
```

### 6. Execute a aplicação

```bash
python run.py
```

Acesse em: **http://localhost:5000**

---

## Credenciais de teste

| E-mail | Senha | Perfil |
|--------|-------|--------|
| admin@sirae.com.br | admin123 | Administrador (TI) |
| ana.lima@sirae.com.br | 123456 | Atendente |
| carlos.m@sirae.com.br | 123456 | Atendente |
| patricia@sirae.com.br | 123456 | Atendente |
| fernanda.p@sirae.com.br | 123456 | Pedagogo |
| rodrigo.b@sirae.com.br | 123456 | Pedagogo |
| marcos.r@sirae.com.br | 123456 | Coordenação |
| juliana.c@sirae.com.br | 123456 | Coordenação |

---

## Estrutura do projeto

```
sirae-project/
├── app/
│   ├── __init__.py          # Factory function, blueprints, extensões
│   ├── utils.py             # Decoradores de controle de acesso
│   ├── models/
│   │   ├── usuario.py       # Entidade Usuario (Flask-Login)
│   │   ├── aluno.py         # Entidade Aluno
│   │   ├── ocorrencia.py    # Entidades Ocorrencia e LogAuditoria
│   │   └── log_admin.py     # Entidade LogAdmin
│   ├── routes/
│   │   ├── auth_routes.py   # Autenticação e perfil do usuário
│   │   ├── main_routes.py   # Ocorrências, dashboard, relatórios
│   │   ├── aluno_routes.py  # CRUD de alunos
│   │   └── admin_routes.py  # Gestão de usuários (TI)
│   ├── static/              # CSS, imagens, uploads
│   └── templates/           # Templates Jinja2
├── config.py                # Configurações da aplicação
├── run.py                   # Ponto de entrada
├── seed.py                  # Dados de exemplo
└── requirements.txt         # Dependências
```

---

## Justificativa de versionamento

O versionamento do SIRAE foi conduzido utilizando o Git como sistema de controle de versão distribuído, com repositório hospedado no GitHub. A estratégia adotada pelo grupo seguiu o modelo de **trunk-based development simplificado**, onde a branch principal (`main`) concentra o código estável e funcional a cada entrega.

Durante o desenvolvimento, cada funcionalidade relevante foi consolidada em commits atômicos e descritivos, facilitando a rastreabilidade das alterações. Os commits foram organizados de forma a refletir incrementos funcionais reais — como a implementação do sistema de ocorrências, do controle de acesso por perfil, do módulo de relatórios e das funcionalidades de segurança como registros sigilosos.

A integridade do código foi garantida por meio de testes manuais após cada incremento antes do commit, evitando que código quebrado fosse consolidado na branch principal. O arquivo `requirements.txt` foi mantido atualizado ao longo de todo o desenvolvimento, garantindo que qualquer membro da equipe pudesse reproduzir o ambiente de execução de forma idêntica.

A separação clara entre o código-fonte da aplicação (`app/`), as configurações (`config.py`), o ponto de entrada (`run.py`) e os dados de seed (`seed.py`) facilitou a divisão de responsabilidades entre os membros e reduziu conflitos de merge. Arquivos sensíveis como credenciais de banco de dados foram mantidos como variáveis de ambiente, nunca versionados diretamente no repositório, seguindo as boas práticas de segurança em projetos de software.

---

## Tecnologias utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.12 + Flask 3.0 |
| ORM / Banco | Flask-SQLAlchemy + MySQL 8 |
| Autenticação | Flask-Login + Werkzeug (hash bcrypt) |
| Frontend | Jinja2 + CSS puro (Design System próprio) |
| Ícones | Lucide Icons (SVG inline) |

