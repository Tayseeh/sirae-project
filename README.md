# SIRAE – Sistema de Registro e Acompanhamento Estudantil

**Projeto Aplicado I — UniSENAI Florianópolis**

---

## O que é o SIRAE?

O SIRAE é uma aplicação web desenvolvida para o setor de apoio estudantil da Faculdade de Tecnologia SENAI Antônio Adolpho Lobbe. O sistema centraliza o registro, acompanhamento e encerramento de ocorrências envolvendo alunos dos cursos técnicos, de graduação e pós-graduação, substituindo o controle manual em planilhas ou documentos avulsos.

### Quem usa o sistema e o que cada perfil faz

| Perfil | O que pode fazer |
|--------|-----------------|
| **Administrador (TI)** | Gerenciar usuários (criar, editar, ativar/desativar), visualizar logs administrativos |
| **Atendente** | Abrir ocorrências, registrar trâmites, anexar documentos, encaminhar para outros membros |
| **Pedagogo** | Acompanhar ocorrências encaminhadas, registrar andamentos |
| **Coordenação** | Visualizar todas as ocorrências, ler notas sigilosas, acessar painel de relatórios e exportar PDF |

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado na sua máquina:

- **Python 3.10 ou superior** — [download](https://www.python.org/downloads/)
- **MySQL 8.0 ou superior** — [download](https://dev.mysql.com/downloads/mysql/)
- **pip** (gerenciador de pacotes Python — já vem com o Python)
- **Git** — [download](https://git-scm.com/downloads)

> ⚠️ O servidor MySQL precisa estar **em execução** antes de qualquer passo de banco de dados abaixo.

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
```

Ative o ambiente — escolha o comando conforme seu sistema operacional:

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

> Quando o ambiente estiver ativo, você verá `(.venv)` no início da linha do terminal.

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Isso instala automaticamente Flask, SQLAlchemy, Flask-Login, o conector MySQL e as demais bibliotecas necessárias.

### 4. Configure o banco de dados

No MySQL, crie o banco de dados (via terminal MySQL ou qualquer cliente como DBeaver/MySQL Workbench):

```sql
CREATE DATABASE sirae_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Copie o arquivo de exemplo de variáveis de ambiente e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` gerado:

```
SECRET_KEY=qualquer-string-longa-e-aleatoria
DATABASE_URL=mysql+mysqlconnector://SEU_USUARIO:SUA_SENHA@localhost/sirae_db
```

> ⚠️ O arquivo `.env` contém suas credenciais e **nunca deve ser enviado ao repositório** — ele já está no `.gitignore`.

### 5. Crie as tabelas e popule os dados iniciais

```bash
python seed.py
```

Este comando cria todas as tabelas no banco e insere usuários e dados de teste prontos para uso.

### 6. Inicie a aplicação

```bash
python run.py
```

Acesse no navegador: **http://localhost:5000**

---

## Credenciais de teste

Use qualquer um dos usuários abaixo para explorar o sistema:

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

> **Dica:** Para ver o sistema completo, faça login como Atendente para abrir uma ocorrência e depois como Coordenação para visualizar relatórios e notas sigilosas.

---

## Estrutura do projeto

```
sirae-project/
├── app/
│   ├── models/
│   │   ├── usuario.py          # Entidade Usuario (autenticação e perfis)
│   │   ├── aluno.py            # Entidade Aluno (dados acadêmicos e pessoais)
│   │   ├── ocorrencia.py       # Entidades Ocorrencia e LogAuditoria
│   │   └── log_admin.py        # Entidade LogAdmin (ações administrativas)
│   ├── routes/
│   │   ├── auth_routes.py      # Login, logout e perfil do usuário
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

O projeto utiliza Git com o modelo de branches por funcionalidade. A branch `main` mantém sempre a versão estável do sistema. O desenvolvimento de novas funcionalidades ocorre em branches separadas, nomeadas de forma descritiva — por exemplo, `feature/cadastro-alunos`, `feature/relatorios` e `fix/filtros-relatorio` — integradas à branch principal somente após validação e testes locais.

Os commits seguem a convenção semântica com prefixos padronizados: `feat:` para novas funcionalidades, `fix:` para correções de bugs, `docs:` para atualizações de documentação e `refactor:` para reestruturações internas sem mudança de comportamento. Essa convenção torna o histórico legível e rastreável por qualquer membro da equipe, permitindo identificar rapidamente o que foi alterado em cada entrega.

O arquivo `.gitignore` foi configurado para excluir o ambiente virtual (`.venv/`), caches do interpretador Python (`__pycache__/`), arquivos de configuração sensíveis com credenciais do banco de dados e uploads de arquivos gerados em tempo de execução. Com isso, apenas o código-fonte e os arquivos essenciais à reprodução do projeto foram versionados no repositório.

A integridade do código foi preservada porque nenhuma alteração foi enviada diretamente à branch `main` sem revisão prévia. Essa abordagem evitou conflitos de código entre os membros da equipe, garantiu que versões incompletas ou com bugs não chegassem à branch principal e permitiu reverter mudanças problemáticas com segurança através do histórico de commits registrado no GitHub. O uso consistente de Pull Requests como etapa obrigatória antes da integração foi fundamental para manter a qualidade e a coerência do código ao longo de todo o desenvolvimento.

---

## Problemas comuns

**Erro ao conectar ao banco de dados**
Verifique se o MySQL está em execução e se as credenciais no arquivo `.env` estão corretas (usuário, senha e nome do banco).

**`ModuleNotFoundError`**
Certifique-se de que o ambiente virtual está ativo (você deve ver `(.venv)` no terminal) e que rodou `pip install -r requirements.txt`.

**Porta 5000 ocupada**
Outro processo está usando a porta. Encerre-o ou altere a porta em `run.py`.
