# SIRAE – Sistema de Registro e Acompanhamento Estudantil

**Grupo 17 | Projeto Aplicado I – UniSENAI 2025/02**

## Descrição

Sistema web para cadastro e acompanhamento de ocorrências do setor de apoio estudantil, desenvolvido com Python, Flask e MySQL.

---

<<<<<<< HEAD
## Pré-requisitos
=======
## 🎯 Composição de Linguagens

| Linguagem | Percentual |
|-----------|-----------|
| HTML      | 53.6%     |
| Python    | 34.6%     |
| CSS       | 11.8%     |

---

## ✨ Funcionalidades Principais

### 👥 **Gestão de Alunos**
- ✅ Cadastro, edição e consulta de alunos
- ✅ Upload e armazenamento de fotos com validação
- ✅ Validação automática de CPF, telefone e matrícula
- ✅ Gestão de dados acadêmicos (série, turma, turno, nível)
- ✅ Gestão de responsáveis (para menores de idade)
- ✅ Busca em tempo real com autocomplete (JSON API)
- ✅ Cálculo automático de idade e identificação de menores

### 📋 **Gestão de Ocorrências**
- ✅ Registro de ocorrências vinculadas a alunos
- ✅ Acompanhamento do status das ocorrências
- ✅ Edição e encerramento de ocorrências
- ✅ Visualização de histórico por aluno

### 👨‍💼 **Painel Administrativo**
- ✅ Gestão de usuários (criar, editar, desativar)
- ✅ Controle de perfis (admin, atendente, coordenação)
- ✅ Visualização de logs de auditoria com filtros
- ✅ Proteção de áreas administrativas por perfil

### 🔐 **Autenticação e Segurança**
- ✅ Login com email e senha
- ✅ Sessões permanentes com timeout de 2 horas
- ✅ Controle de acesso baseado em perfil
- ✅ Criptografia de senhas com Werkzeug
- ✅ Proteção contra XSS e ataques comuns
- ✅ Páginas de erro customizadas (404, 403, 500)
- ✅ Log de auditoria completo
- ✅ Conformidade com LGPD

---

## 🚀 Quick Start

### Pré-requisitos
>>>>>>> d401b0bd57eca2ce68d31ecf85f02cbb46fbc643

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

<<<<<<< HEAD
Os commits seguem uma convenção descritiva: `feat:`, `fix:`, `docs:`, `refactor:`, indicando claramente o tipo de mudança. O histórico de commits comprova a participação de cada membro nas respectivas áreas de responsabilidade. O arquivo `.gitignore` foi configurado para excluir o ambiente virtual (`.venv/`), arquivos de configuração sensíveis e caches Python, garantindo que apenas o código-fonte e os arquivos essenciais sejam versionados. A integridade do código é mantida porque nenhuma alteração vai direto ao `main` sem revisão de ao menos um outro membro da equipe.
=======
1. **Factory Pattern**
   - Função `create_app()` em `app/__init__.py` cria a instância da aplicação Flask com todas as configurações

2. **Blueprint Architecture**
   - Separação modular por funcionalidade: `auth_bp`, `main_bp`, `aluno_bp`, `admin_bp`
   - Cada blueprint tem seu próprio namespace de rotas

3. **MVC (Model-View-Controller)**
   - **Models:** `app/models/` - Entidades e relacionamentos
   - **Views:** `app/templates/` - Templates HTML
   - **Controllers:** `app/routes/` - Lógica de negócio

4. **POO (Programação Orientada a Objetos)**
   - Classes de entidade com encapsulamento
   - Herança: `Usuario` herda de `UserMixin`
   - Propriedades calculadas: `Usuario.is_admin`, `Aluno.idade`
   - Relacionamentos: `Aluno` ↔ `Ocorrencia`

---

## 🗄️ Modelos de Dados

### **Usuario** (Autenticação)
```python
- id: Integer (PK)
- email: String (unique)
- password_hash: String (criptografado)
- nome: String
- perfil: String (admin | atendente | coordenacao)
- ativo: Boolean

Métodos:
- set_password(password) → criptografa a senha
- check_password(password) → valida a senha
- is_admin, is_atendente, is_coordenador → propriedades de tipo
```

### **Aluno** (Gestão Estudantil)
```python
Dados Pessoais:
- id: Integer (PK)
- nome: String (obrigatório)
- data_nascimento: Date
- cpf: String (formatado: 000.000.000-00)
- email: String
- telefone: String (formatado: (XX) XXXXX-XXXX)
- foto: String (caminho para upload)

Dados Acadêmicos:
- matricula: String (unique)
- nivel: String (fundamental | médio)
- serie: String (6º ano | 1º ano EM, etc)
- turma: String (A | B | C)
- turno: String (manhã | tarde | noite)

Responsável (para menores):
- responsavel_nome: String
- responsavel_parentesco: String
- responsavel_cpf: String
- responsavel_contato: String
- responsavel_email: String

Controle:
- ativo: Boolean
- criado_em: DateTime

Propriedades Calculadas:
- idade → calcula idade a partir da data de nascimento
- menor_de_idade → boolean se idade < 18
- serie_completa → "6º ano EF · Turma A · manhã"
- total_ocorrencias → quantidade de registros
- ocorrencias_ativas → lista de ocorrências abertas
```

### **Ocorrencia** (Registros de Eventos)
```python
- id: Integer (PK)
- aluno_id: Integer (FK → Aluno)
- descricao: Text
- status: String (aberta | em_acompanhamento | encerrada)
- data_criacao: DateTime
- data_encerramento: DateTime
- usuario_id: Integer (FK → Usuario que criou)

Relacionamento:
- Aluno pode ter múltiplas ocorrências
- Cada ocorrência pertence a um aluno
```

### **LogAuditoria** (Rastreabilidade)
```python
- id: Integer (PK)
- usuario_id: Integer (FK)
- acao: String (criar | editar | deletar | consultar)
- tabela: String (alunos | ocorrencias | usuarios)
- registro_id: Integer (qual registro foi afetado)
- data_hora: DateTime

Propósito:
- Rastrear todas as alterações no sistema
- Conformidade com LGPD
- Auditoria e compliance
```

---

## 🌐 Rotas Principais

### **Autenticação**
```
POST   /auth/login              Login de usuários
GET    /auth/logout             Logout
```

### **Alunos**
```
GET    /alunos/                 Listar alunos (com filtros)
GET    /alunos/novo             Formulário novo aluno
POST   /alunos/novo             Criar novo aluno
GET    /alunos/editar/<id>      Formulário editar aluno
POST   /alunos/editar/<id>      Atualizar aluno
GET    /alunos/perfil/<id>      Ver perfil do aluno
GET    /alunos/busca-json       Busca JSON (autocomplete)
```

### **Ocorrências**
```
GET    /ocorrencias/            Listar ocorrências
GET    /ocorrencias/novo        Formulário nova ocorrência
POST   /ocorrencias/novo        Criar ocorrência
GET    /ocorrencias/editar/<id> Formulário editar
POST   /ocorrencias/editar/<id> Atualizar ocorrência
GET    /ocorrencias/encerrar/<id> Encerrar ocorrência
```

### **Painel Admin**
```
GET    /admin/usuarios          Listar usuários
GET    /admin/usuarios/novo     Formulário novo usuário
POST   /admin/usuarios/novo     Criar usuário
GET    /admin/usuarios/editar/<id> Editar usuário
GET    /admin/usuarios/desativar/<id> Desativar usuário
GET    /admin/logs              Visualizar logs (com filtros)
```

---

## 🔐 Segurança

### **Implementações de Segurança**

✅ **Autenticação**
- Login obrigatório com email e senha
- Senhas criptografadas com `Werkzeug.generate_password_hash()`
- Sessões com timeout de 2 horas

✅ **Autorização**
- Decorador `@apenas_admin` para rotas administrativas
- Rotas protegidas com `@login_required`
- Controle de acesso por perfil de usuário

✅ **Validação de Entrada**
- Validação de CPF (11 dígitos)
- Validação de telefone (10 ou 11 dígitos)
- Sanitização contra XSS
- Upload de fotos apenas com extensões permitidas

✅ **Auditoria**
- Log de todas as ações em `LogAuditoria`
- Rastreamento de quem acessou/alterou cada registro
- Conformidade com LGPD

✅ **Proteção de Dados**
- Backups automáticos no Google Drive
- Dados pessoais criptografados onde necessário
- Permissões por perfil (atendente ≠ admin)

---
>>>>>>> d401b0bd57eca2ce68d31ecf85f02cbb46fbc643
