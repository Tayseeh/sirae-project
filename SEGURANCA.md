# Segurança — SIRAE

Documentação das práticas de segurança adotadas no sistema, em conformidade com a LGPD.

---

## Autenticação

### Hash de senhas
As senhas nunca são armazenadas em texto puro. O sistema usa o algoritmo **PBKDF2-SHA256** via Werkzeug:

```python
# Geração do hash
def set_password(self, password):
    self.password_hash = generate_password_hash(password)

# Verificação
def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

### Sessões
- Sessões gerenciadas pelo Flask-Login com timeout de **2 horas** de inatividade
- Sessões são permanentes para evitar logout ao fechar o navegador acidentalmente
- Logout invalida a sessão imediatamente

### Bloqueio de usuários inativos
O login verifica se o usuário está ativo antes de autenticar:

```python
if user and user.ativo and user.check_password(password):
    login_user(user)
```

Usuários desativados pelo administrador não conseguem acessar o sistema mesmo com senha correta.

---

## Controle de acesso

Cada rota é protegida por decoradores que verificam o perfil do usuário:

```python
@apenas_admin        # Somente TI
@apenas_coordenador  # Somente coordenação
@nao_admin          # Todos exceto TI
```

Tentativas de acesso a rotas não autorizadas retornam erro 403.

---

## Upload de arquivos

Todos os uploads passam por validação antes de salvar:

- **Formatos permitidos:** PDF, JPG, JPEG, PNG, DOC, DOCX
- **Tamanho máximo:** 5MB por arquivo
- **Sanitização:** nomes de arquivo são sanitizados com `secure_filename()` do Werkzeug para evitar path traversal

```python
nome_seguro = secure_filename(arquivo.filename)
nome = f"{usuario_id}_{int(time.time())}_{nome_seguro}"
```

---

## Notas sigilosas

Registros marcados como sigilosos em `logs_auditoria` são visíveis **apenas para o perfil coordenação**. Atendentes e pedagogos não têm acesso a esse conteúdo, mesmo que estejam visualizando a mesma ocorrência.

---

## Credenciais

- Credenciais do banco de dados ficam no arquivo `.env`, que nunca é versionado no repositório
- O `.gitignore` garante que o `.env` não seja enviado ao GitHub acidentalmente
- O arquivo `.env.example` serve como modelo sem dados sensíveis

---

## Rastreabilidade e LGPD

Toda ação no sistema gera um registro em `logs_auditoria` ou `logs_admin`:

- Quem fez
- O que fez
- Quando fez

Isso garante rastreabilidade completa e atende ao princípio de responsabilização da **Lei Geral de Proteção de Dados (Lei nº 13.709/2018)**.

Dados pessoais de alunos (CPF, data de nascimento, contato de responsável) são acessíveis apenas por usuários autenticados e com perfil adequado.

---

## Testes de segurança

A suite de testes em `test_sirae.py` valida automaticamente:

- Bloqueio de login com usuário inativo
- Rejeição de acesso a rotas protegidas sem autenticação
- Rejeição de acesso a rotas de perfil incorreto
- Validação de uploads com formato e tamanho inválidos
