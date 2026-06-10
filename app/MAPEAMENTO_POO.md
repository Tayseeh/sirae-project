# Mapeamento de POO — SIRAE

Identificação e justificativa de como os quatro pilares da Programação Orientada a Objetos foram aplicados no SIRAE.

---

## 1. Encapsulamento

O encapsulamento protege os dados internos das classes e expõe apenas o necessário para o restante do sistema.

### Classe `Usuario`
A senha nunca é armazenada ou acessada diretamente. Dois métodos encapsulam toda a lógica de segurança:

```python
def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

Nenhuma rota ou controller acessa `password_hash` diretamente — toda interação passa por esses métodos.

### Classe `Aluno`
A lógica de menoridade é encapsulada como propriedade calculada, sem campo adicional no banco:

```python
@property
def menor_de_idade(self):
    return self.idade is not None and self.idade < 18
```

### Classe `Ocorrencia`
O encerramento de uma ocorrência encapsula todas as operações necessárias em um único método:

```python
def encerrar(self):
    self.status = 'encerrada'
    self.data_encerramento = datetime.now(timezone.utc)
```

---

## 2. Herança

A herança é utilizada para reaproveitar comportamentos já implementados nos frameworks.

### `db.Model` — SQLAlchemy
Todas as classes de entidade herdam de `db.Model`, que fornece o mapeamento objeto-relacional completo: geração automática de queries, gerenciamento de sessão e criação de tabelas.

### `UserMixin` — Flask-Login
A classe `Usuario` herda também de `UserMixin`, que adiciona os métodos `is_authenticated`, `is_active`, `is_anonymous` e `get_id()`, necessários para o sistema de sessões autenticadas.

```python
class Usuario(db.Model, UserMixin):
    ...
```

Essa herança múltipla elimina código repetitivo e garante compatibilidade com os frameworks sem implementação manual desses comportamentos.

---

## 3. Abstração

A abstração oculta a complexidade interna e expõe apenas interfaces simples.

### Função `_log()`
Abstrai por completo o registro de auditoria. Nenhuma rota precisa conhecer os detalhes do model `LogAuditoria`:

```python
def _log(ocorrencia_id, acao, descricao, sigiloso=False, anexo_log=None):
    db.session.add(LogAuditoria(
        ocorrencia_id=ocorrencia_id,
        usuario_id=current_user.id,
        acao=acao,
        descricao_acao=descricao,
        sigiloso=sigiloso,
        anexo_log=anexo_log
    ))
```

### Decoradores de controle de acesso
Os decoradores `@apenas_admin`, `@nao_admin` e `@apenas_coordenador` abstraem toda a lógica de autorização por perfil:

```python
def apenas_admin(f):
    return requer_perfil('admin')(f)
```

Aplicados diretamente nas rotas de forma declarativa, eliminam repetição de verificações condicionais em cada endpoint.

---

## 4. Polimorfismo

O polimorfismo permite que o mesmo código funcione com diferentes tipos e contextos.

### Método `encerrar()`
Pode ser chamado por qualquer perfil autorizado (atendente, pedagogo ou coordenação) com o mesmo resultado:

```python
def encerrar(self):
    self.status = 'encerrada'
    self.data_encerramento = datetime.now(timezone.utc)
```

### Templates Jinja2
Os mesmos templates renderizam conteúdo diferente dependendo do perfil do usuário logado, sem duplicação de código:

```html
{% if current_user.perfil == 'coordenacao' %}
    <!-- exibe notas sigilosas -->
{% endif %}
```

### Rotas de ocorrência
As rotas de criar, editar, encaminhar e encerrar operam sobre o mesmo objeto `Ocorrencia` com comportamentos distintos conforme o estado atual e o perfil do usuário autenticado.

---

## Benefícios para manutenção e escalabilidade

| Pilar | Benefício |
|---|---|
| Encapsulamento | Mudanças internas (ex: trocar algoritmo de hash) não afetam o restante do sistema |
| Herança | Novos models seguem o mesmo contrato de persistência sem código adicional |
| Abstração | Adicionar um novo tipo de log não exige mudanças nas rotas |
| Polimorfismo | Novos perfis de usuário podem ser adicionados sem reescrever templates |
