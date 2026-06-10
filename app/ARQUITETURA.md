# Arquitetura — SIRAE

## Visão geral

O SIRAE segue o padrão arquitetural **MVC (Model-View-Controller)**, implementado com Flask e organizado em módulos separados por responsabilidade.

```
sirae-project/
├── app/
│   ├── models/        # Model — entidades e regras de dados
│   ├── routes/        # Controller — lógica de negócio e rotas HTTP
│   ├── templates/     # View — templates HTML com Jinja2
│   ├── static/        # Arquivos estáticos (CSS, imagens)
│   ├── utils.py       # Decoradores de controle de acesso
│   └── __init__.py    # Factory da aplicação Flask
├── config.py          # Configurações da aplicação
├── run.py             # Ponto de entrada
└── seed.py            # Carga inicial de dados
```

---

## Camadas

### Model (`app/models/`)
Responsável pela definição das entidades e pela comunicação com o banco de dados via SQLAlchemy.

| Arquivo | Entidades |
|---|---|
| `usuario.py` | `Usuario` — autenticação e perfis de acesso |
| `aluno.py` | `Aluno` — dados acadêmicos e pessoais |
| `ocorrencia.py` | `Ocorrencia`, `LogAuditoria` — ciclo de vida do atendimento |
| `log_admin.py` | `LogAdmin` — ações administrativas |

### Controller (`app/routes/`)
Responsável por receber as requisições HTTP, aplicar as regras de negócio e retornar as respostas.

| Arquivo | Responsabilidade |
|---|---|
| `auth_routes.py` | Login, logout e edição de perfil |
| `main_routes.py` | Dashboard, ocorrências e relatórios |
| `aluno_routes.py` | CRUD de alunos e busca por JSON |
| `admin_routes.py` | Gestão de usuários e logs administrativos |

### View (`app/templates/`)
Templates HTML renderizados pelo Jinja2 com os dados enviados pelos controllers.

---

## Controle de acesso

Definido em `app/utils.py` através de decoradores aplicados diretamente nas rotas:

| Decorador | Quem pode acessar |
|---|---|
| `@apenas_admin` | Somente perfil `admin` |
| `@apenas_coordenador` | Somente perfil `coordenacao` |
| `@nao_admin` | `atendente`, `pedagogia` e `coordenacao` |

---

## Fluxo principal

```
Usuário → HTTP Request
    → Flask Router
        → Decorador de autenticação (Flask-Login)
            → Decorador de perfil (utils.py)
                → Função de rota (routes/)
                    → Model / SQLAlchemy
                        → MySQL
                    ← Dados
                ← Template renderizado (Jinja2)
        ← HTTP Response
```

---

## Tecnologias e justificativas

| Tecnologia | Função | Justificativa |
|---|---|---|
| Flask | Framework web | Leve, flexível e com grande ecossistema |
| SQLAlchemy | ORM | Abstrai o SQL e garante portabilidade |
| Flask-Login | Autenticação | Gerencia sessões de forma segura |
| Werkzeug | Segurança | Hash de senhas com PBKDF2-SHA256 |
| Jinja2 | Templates | Integrado ao Flask, sintaxe simples |
| MySQL | Banco de dados | Confiável, amplamente utilizado e compatível |
| python-dotenv | Configuração | Mantém credenciais fora do código-fonte |
