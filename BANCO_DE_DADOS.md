# Banco de Dados — SIRAE

## Tecnologia utilizada

O SIRAE utiliza **MySQL 8.0** como banco de dados relacional, integrado ao Flask através do **SQLAlchemy** (ORM) e do **Flask-SQLAlchemy**.

---

## Tabelas

### `usuarios`
Armazena os membros da equipe que acessam o sistema.

| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único |
| email | String(100) | E-mail de login (único) |
| password_hash | String(200) | Senha criptografada com PBKDF2-SHA256 |
| nome | String(100) | Nome completo |
| perfil | String(20) | Nível de acesso: `admin`, `atendente`, `pedagogia`, `coordenacao` |
| foto | String(200) | Caminho da foto de perfil |
| telefone | String(20) | Telefone de contato |
| ramal | String(10) | Ramal interno |
| cargo | String(100) | Cargo na instituição |
| ultimo_login | DateTime | Data e hora do último acesso |
| ativo | Boolean | Se o usuário está ativo no sistema |

---

### `alunos`
Armazena os dados acadêmicos e pessoais dos alunos.

| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único |
| nome | String(100) | Nome completo do aluno |
| cpf | String(14) | CPF formatado (único) |
| matricula | String(20) | Matrícula acadêmica (única) |
| nivel | String(30) | Nível de ensino: `tecnico`, `graduacao`, `pos` |
| curso | String(100) | Nome do curso |
| serie | String(30) | Semestre ou ano atual |
| turma | String(10) | Turma (A, B, C...) |
| turno | String(10) | Turno: manhã, tarde ou noite |
| data_nascimento | Date | Data de nascimento (usada para calcular menoridade) |
| email | String(100) | E-mail do aluno |
| telefone | String(20) | Telefone do aluno |
| foto | String(200) | Caminho da foto do aluno |
| tipo_contato | String(20) | `responsavel` (menor) ou `emergencia` (adulto) |
| responsavel_nome | String(100) | Nome do responsável ou contato de emergência |
| responsavel_parentesco | String(30) | Grau de parentesco |
| responsavel_cpf | String(14) | CPF do responsável |
| responsavel_contato | String(20) | Telefone do responsável |
| responsavel_email | String(100) | E-mail do responsável |
| ativo | Boolean | Se o aluno está ativo |
| criado_em | DateTime | Data de cadastro |

---

### `ocorrencias`
Registra o ciclo de vida completo de cada atendimento.

| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único |
| aluno_id | Integer (FK) | Referência ao aluno |
| tipo | String(50) | Tipo: Disciplinar, Saúde, Financeiro, Evasão, etc. |
| descricao | Text | Descrição detalhada da ocorrência |
| anexo_arquivo | String(200) | Caminho do arquivo anexado na abertura |
| status | String(20) | Estado: `aberta`, `em_andamento`, `encerrada` |
| criado_por_id | Integer (FK) | Usuário que abriu a ocorrência |
| responsavel_id | Integer (FK) | Usuário responsável no momento atual |
| data_criacao | DateTime | Data e hora de abertura |
| data_encerramento | DateTime | Data e hora de encerramento |

---

### `logs_auditoria`
Histórico imutável de todas as ações em cada ocorrência.

| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único |
| ocorrencia_id | Integer (FK) | Referência à ocorrência |
| usuario_id | Integer (FK) | Usuário que realizou a ação |
| acao | String(50) | Tipo de ação: `criada`, `atualizada`, `encaminhada`, `encerrada` |
| descricao_acao | Text | Descrição detalhada da ação |
| sigiloso | Boolean | Se o registro é visível apenas para a coordenação |
| anexo_log | String(200) | Caminho de arquivo anexado neste log |
| data_hora | DateTime | Data e hora da ação |

---

### `logs_admin`
Registra ações administrativas realizadas pelo perfil TI.

| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único |
| usuario_id | Integer (FK) | Administrador que realizou a ação |
| acao | String(50) | Tipo: `criou_usuario`, `editou_usuario`, `desativou_usuario` |
| alvo_nome | String(100) | Nome do usuário afetado |
| descricao | Text | Descrição completa da ação |
| data_hora | DateTime | Data e hora da ação |

---

## Relacionamentos

```
usuarios (1) ──── (N) ocorrencias [criado_por_id]
usuarios (1) ──── (N) ocorrencias [responsavel_id]
usuarios (1) ──── (N) logs_auditoria
usuarios (1) ──── (N) logs_admin
alunos   (1) ──── (N) ocorrencias
ocorrencias (1) ── (N) logs_auditoria
```

---

## Decisões de modelagem

**Por que dois campos de usuário em `ocorrencias`?**
`criado_por_id` nunca muda — registra quem abriu a ocorrência. `responsavel_id` muda a cada encaminhamento — registra quem está cuidando no momento. Isso permite rastrear a origem e o estado atual de forma independente.

**Por que `logs_auditoria` é separado de `ocorrencias`?**
Cada ocorrência pode ter múltiplos registros de andamento ao longo do tempo. Manter em tabela separada evita duplicação de dados e permite histórico ilimitado sem alterar o registro principal.

**Por que `logs_admin` é separado de `logs_auditoria`?**
Ações administrativas (criar/editar usuários) não estão relacionadas a nenhuma ocorrência específica. Separar mantém cada log com responsabilidade clara e facilita consultas independentes.

**Por que `sigiloso` em `logs_auditoria`?**
Permite que a coordenação registre andamentos internos visíveis apenas ao seu perfil, sem expor informações sensíveis para atendentes e pedagogos.
