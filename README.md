# SIRAE – Sistema de Registro e Acompanhamento Estudantil

**Grupo 17 | Projeto Aplicado I – UniSENAI 2025/02**

Alunos: Celso Augusto Cândido Cacholi, Renan William Andrade Leal Cardoso, Tayse Espindola, Pedro Gonçalves e Eduardo Piassabussu

## 📋 Descrição

Sistema web para cadastro e acompanhamento de ocorrências do setor de apoio estudantil, desenvolvido com Python, Flask e MySQL. O SIRAE centraliza o registro de eventos estudantis, substituindo planilhas por uma solução organizada, segura e com rastreabilidade completa.

**Problema resolvido:** O setor de apoio estudantil da Faculdade de Tecnologia SENAI – Antônio Adolpho Lobbe realizava registros de ocorrências em planilhas, dificultando organização, consulta e controle das informações.

**Solução:** Aplicação web com controle de acesso por perfil, autenticação segura, gestão de alunos, registro de ocorrências, painel administrativo e logs de auditoria em conformidade com a LGPD.

---

## 🎯 Composição de Linguagens

| Linguagem | Percentual |
|-----------|-----------|
| HTML      | 53%       |
| Python    | 35.3%     |
| CSS       | 11.7%     |

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

- Python 3.10 ou superior
- MySQL 8.0 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Instalação em 6 Passos

#### **1. Clone o repositório**

```bash
git clone https://github.com/Tayseeh/sirae-project.git
cd sirae-project
```

#### **2. Crie e ative o ambiente virtual**

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar no Windows
.venv\Scripts\activate

# Ativar no Linux/Mac
source .venv/bin/activate
```

#### **3. Instale as dependências**

```bash
pip install -r requirements.txt
```

#### **4. Configure o banco de dados**

No MySQL (via terminal ou MySQL Workbench), crie o banco:

```sql
CREATE DATABASE sirae_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Edite o arquivo `config.py` com suas credenciais MySQL:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://SEU_USUARIO:SUA_SENHA@localhost/sirae_db'
```

**Exemplo:**
```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:admin123@localhost/sirae_db'
```

#### **5. Crie as tabelas e popule com dados iniciais**

```bash
python seed.py
```

Isso criará automaticamente as tabelas e inserirá usuários de teste.

#### **6. Execute a aplicação**

```bash
python run.py
```

A aplicação estará disponível em: **http://localhost:5000**

---

## 🔑 Credenciais de Teste

| Usuário | Email | Senha | Perfil | Acesso |
|---------|-------|-------|--------|--------|
| Administrador | admin@sirae.com | admin123 | admin | Painel completo + gestão de usuários + logs |
| Atendente | atendente@sirae.com | 123456 | atendente | Gestão de alunos e ocorrências |
| Coordenadora | coord@sirae.com | 123456 | coordenacao | Visualização de relatórios e ocorrências |

**Teste de fluxo recomendado:**
1. Faça login como `admin@sirae.com`
2. Crie um novo aluno em **Alunos → Novo**
3. Registre uma ocorrência para o aluno
4. Faça logout e teste com outro perfil

---

## 📦 Dependências Principais

```
Flask==3.0.0              # Framework web
Flask-SQLAlchemy==3.1.1   # ORM para banco de dados
Flask-Login==0.6.3        # Autenticação e sessões
mysql-connector-python==8.3.0  # Driver MySQL
Werkzeug==3.0.1           # Utilitários Flask (segurança)
```

Veja `requirements.txt` para a lista completa.

---

## 📂 Estrutura do Projeto

```
sirae-project/
├── app/
│   ├── models/                  # Camada de dados (POO)
│   │   ├── __init__.py
│   │   ├── usuario.py           # Modelo Usuario (autenticação)
│   │   ├── aluno.py             # Modelo Aluno (gestão estudantil)
│   │   └── ocorrencia.py        # Modelos Ocorrencia e LogAuditoria
│   │
│   ├── routes/                  # Rotas (controllers)
│   │   ├── __init__.py
│   │   ├── auth_routes.py       # Login/Logout
│   │   ├── main_routes.py       # Ocorrências (CRUD)
│   │   ├── aluno_routes.py      # Alunos (CRUD + upload)
│   │   └── admin_routes.py      # Painel administrativo
│   │
│   ├── templates/               # Views (HTML com Jinja2)
│   │   ├── base.html            # Template base
│   │   ├── base_login.html      # Template login
│   │   ├── dashboard.html       # Dashboard principal
│   │   ├── alunos/
│   │   │   ├── listar.html      # Listagem de alunos
│   │   │   ├── form.html        # Criar/editar aluno
│   │   │   └── perfil.html      # Perfil do aluno
│   │   ├── admin/
│   │   │   ├── usuarios.html    # Gestão de usuários
│   │   │   ├── form_usuario.html
│   │   │   └── logs.html        # Logs de auditoria
│   │   ├── auth/
│   │   │   └── login.html       # Página de login
│   │   └── errors/
│   │       ├── 404.html         # Página não encontrada
│   │       ├── 403.html         # Acesso proibido
│   │       └── 500.html         # Erro do servidor
│   │
│   ├── static/                  # Arquivos estáticos
│   │   ├── css/
│   │   │   └── style.css        # Estilos CSS
│   │   ├── img/                 # Imagens e logos
│   │   └── uploads/             # Fotos de alunos (gerado dinamicamente)
│   │
│   ├── utils.py                 # Funções utilitárias e decoradores
│   ├── seed.py                  # Script para popular dados iniciais
│   └── __init__.py              # Factory da aplicação
│
├── config.py                    # Configurações (banco, sessão, chaves)
├── run.py                       # Ponto de entrada da aplicação
├── criar_usuario.py             # Utilitário: criar usuários via CLI
├── requirements.txt             # Dependências Python
├── gitignore.txt                # Arquivo .gitignore
└── README.md                    # Este arquivo
```

---

## 🏗️ Arquitetura e Padrões de Projeto

### **Padrões Utilizados**

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

## 📊 Estratégia de Versionamento

O projeto adota o modelo **Git Flow Simplificado** com branches por funcionalidade:

### **Estrutura de Branches**
- **`main`** - Versão estável e em produção
- **`develop`** - Integração de features, branch de desenvolvimento
- **`feature/***`** - Cada funcionalidade em sua própria branch
- **`bugfix/***`** - Correções de bugs
- **`hotfix/***`** - Correções críticas para produção

### **Convenção de Commits**

Seguimos o padrão **Conventional Commits**:

```
feat(scope): descrição breve
fix(scope): descrição breve
docs(scope): descrição breve
style(scope): descrição breve
refactor(scope): descrição breve
test(scope): descrição breve
chore(scope): descrição breve
```

**Exemplos:**
```bash
git commit -m "feat(alunos): criar rota de busca com autocomplete

- Implementar busca JSON para nome e matrícula
- Busca case-insensitive com ilike
- Limite de 10 resultados
- Closes #15"
```

```bash
git commit -m "fix(auth): corrigir timeout de sessão

- Aumentar PERMANENT_SESSION_LIFETIME para 2 horas
- Adicionar make_session_permanent antes de cada request
- Closes #23"
```

### **Fluxo de Trabalho**

1. **Criar issue** no GitHub descrevendo a tarefa
2. **Criar branch** a partir de `develop`: `git checkout -b feature/descricao develop`
3. **Fazer commits** com mensagens descritivas e referência à issue
4. **Push** para o repositório: `git push origin feature/descricao`
5. **Criar Pull Request** (PR) da feature para `develop`
6. **Code Review** por pelo menos 1 membro
7. **Merge** para `develop` após aprovação
8. **Deletar branch** após merge
9. **Release para main** quando versão está pronta

### **Garantia de Integridade do Código**

✅ **Histórico de Commits**
- Todos os membros fazem commits com suas credenciais GitHub
- Cada commit tem mensagem descritiva e referência a issue
- Histórico comprova participação ativa de cada membro

✅ **Code Review**
- Toda mudança passa por PR
- Mínimo 1 aprovação antes de merge
- Revisão garante qualidade e conformidade

✅ **Branch Protection**
- `main` protegida: requer PR e review
- Nenhum push direto para `main`
- Histórico linear e auditável

✅ **Testes e Validação**
- Testes unitários em `tests/`
- Validações nos modelos
- Integração contínua (CI) via GitHub Actions

### **Participação dos Membros**

| Membro | Função | Branches | Commits Estimados |
|--------|--------|----------|------------------|
| Celso Augusto | Banco de Dados | `feature/db-models` | 8-10 |
| Renan William | Arquitetura | `feature/architecture` | 6-8 |
| Tayse Espindola | Backend/UX | `feature/auth`, `feature/alunos`, `feature/admin` | 12-15 |
| Pedro Gonçalves | Integração/Git | `release/v1.0`, PRs, Documentação | 8-10 |
| Eduardo Piassabussu | Testes/Segurança | `feature/security`, `tests/` | 6-8 |

Cada integrante trabalha em suas branches de feature, fazendo commits com suas credenciais pessoais do GitHub. O histórico de commits comprova a participação ativa de todos na construção do projeto.

---

## 💰 Análise Financeira (AV04)

### **CAPEX (Investimento Inicial)**
- Pessoal: R$ 8.500,00 (340 horas)
- Infraestrutura inicial: R$ 40,00 (domínio)
- Ferramentas (1º mês): R$ 48,33
- **Total: R$ 8.588,33**

### **OPEX (Custos Operacionais/Mês)**
- VPS Hospedagem: R$ 30,00
- Backup Google Drive: R$ 15,00
- Manutenção: R$ 120,00
- **Total/mês: R$ 165,00**

### **Modelo de Receita (SaaS)**
- 5 instituições × R$ 250,00/mês = R$ 1.250,00/mês
- **Receita Anual: R$ 15.000,00**

### **ROI e Payback**
- **ROI: 151%** (retorno de 151% no primeiro ano)
- **Payback: ~8 meses** (retorno do investimento em 8 meses)

*Veja documento AV04 completo para análise detalhada de viabilidade, riscos e contingências.*

---

## 🎥 Vídeo de Demonstração

[Link do vídeo no YouTube - A adicionar]

O vídeo contém:
- **Parte Comercial:** Problema, solução e viabilidade financeira
- **Parte Técnica:** Demonstração das funcionalidades do sistema
- **Participação:** Todos os membros do grupo

---

## 📚 Documentação Adicional

- **VERSIONAMENTO.md** - Detalhes sobre estratégia de Git (10+ linhas)
- **POO.md** - Mapeamento dos pilares de Programação Orientada a Objetos (15+ linhas)
- **RASTREABILIDADE.md** - Matriz de requisitos vs implementação
- **AV04.pdf** - Análise financeira completa
- **CONTRIBUTING.md** - Guia para contribuidores

---

## 🐛 Troubleshooting

### **Erro: "ModuleNotFoundError: No module named 'flask'"**
```bash
# Ative o ambiente virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### **Erro: "Can't connect to MySQL server"**
- Verifique se MySQL está rodando
- Confirme usuário, senha e host em `config.py`
- Crie o banco de dados: `CREATE DATABASE sirae_db`

### **Erro: "ModuleNotFoundError: No module named 'mysql'"**
```bash
pip install mysql-connector-python
```

### **Aplicação não inicia no localhost:5000**
- Verifique se a porta 5000 não está em uso
- Tente: `python run.py --port 5001`
- Ou matando processo: `lsof -i :5000` (Linux/Mac)

---

## 📝 Licença

Projeto desenvolvido para fins acadêmicos na Faculdade de Tecnologia SENAI.

---

## 👥 Contato e Suporte

**Grupo 17 - Projeto Aplicado I**
- Celso Augusto Cândido Cacholi
- Renan William Andrade Leal Cardoso
- Tayse Espindola
- Pedro Gonçalves
- Eduardo Piassabussu

**Repositório:** https://github.com/Tayseeh/sirae-project

---

## 📅 Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0.0 | Jun 2026 | Release inicial com funcionalidades core |
| 0.2.0 | Jun 2026 | Adição de painel admin e gestão de usuários |
| 0.1.0 | Jun 2026 | Versão inicial com modelos e rotas básicas |

---

**Última atualização:** 08/06/2026
