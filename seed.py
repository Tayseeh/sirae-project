"""
seed.py — Script de carga inicial de dados do SIRAE
Autor: Celso Augusto Cândido Cacholi
Função: Banco de Dados e Modelagem

Descrição:
    Este script cria todas as tabelas no banco de dados e popula com dados
    fictícios para fins de teste e demonstração do sistema. Deve ser executado
    uma única vez após a configuração do banco de dados.

Execução:
    python seed.py

Pré-requisitos:
    - Banco de dados criado conforme README.md
    - Arquivo .env configurado com DATABASE_URL

O script é idempotente: verifica se os registros já existem antes de inserir,
evitando duplicações caso seja executado mais de uma vez.
"""

from app import create_app, db
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from app.models.ocorrencia import Ocorrencia, LogAuditoria
from app.models.log_admin import LogAdmin
from datetime import datetime, timedelta, timezone

app = create_app()

with app.app_context():
    # Cria as tabelas se não existirem
    db.create_all()

    # ─────────────────────────────────────────
    # USUÁRIOS
    # Cada usuário representa um membro da equipe de apoio estudantil.
    # Perfis disponíveis: admin, atendente, pedagogia, coordenacao
    # ─────────────────────────────────────────
    usuarios_data = [
        dict(email='admin@sirae.com.br',      nome='Administrador',          perfil='admin',
             cargo='Analista de TI',        telefone='(16) 3301-1000',     ramal='2000', senha='admin123'),
        dict(email='ana.lima@sirae.com.br',   nome='Ana Lima',               perfil='atendente',
             cargo='Atendente do Setor de Apoio', telefone='(16) 99101-1111', ramal='2011', senha='123456'),
        dict(email='carlos.m@sirae.com.br',   nome='Carlos Menezes',         perfil='atendente',
             cargo='Assistente Estudantil', telefone='(16) 99202-2222',    ramal='2012', senha='123456'),
        dict(email='patricia@sirae.com.br',   nome='Patrícia Souza',         perfil='atendente',
             cargo='Atendente do Setor de Apoio', telefone='(16) 99303-3333', ramal='2013', senha='123456'),
        dict(email='fernanda.p@sirae.com.br', nome='Fernanda Prado',         perfil='pedagogia',
             cargo='Pedagoga',              telefone='(16) 99404-4444',    ramal='2021', senha='123456'),
        dict(email='rodrigo.b@sirae.com.br',  nome='Rodrigo Bastos',         perfil='pedagogia',
             cargo='Pedagogo',              telefone='(16) 99505-5555',    ramal='2022', senha='123456'),
        dict(email='marcos.r@sirae.com.br',   nome='Marcos Ribeiro',         perfil='coordenacao',
             cargo='Coordenador Pedagógico', telefone='(16) 99606-6666',   ramal='2031', senha='123456'),
        dict(email='juliana.c@sirae.com.br',  nome='Juliana Cardoso',        perfil='coordenacao',
             cargo='Coordenadora de Apoio', telefone='(16) 99707-7777',   ramal='2032', senha='123456'),
    ]

    usuarios = {}
    print("\n── USUÁRIOS ─────────────────────────────")
    for u in usuarios_data:
        # Verifica se o usuário já existe antes de inserir
        ex = Usuario.query.filter_by(email=u['email']).first()
        if not ex:
            novo = Usuario(email=u['email'], nome=u['nome'], perfil=u['perfil'],
                           cargo=u['cargo'], telefone=u['telefone'], ramal=u['ramal'])
            novo.set_password(u['senha'])
            db.session.add(novo)
            db.session.flush()
            usuarios[u['email']] = novo
            print(f"  ✓ {u['nome']:<28} [{u['perfil']:<12}] ramal {u['ramal']}")
        else:
            usuarios[u['email']] = ex
            print(f"  — Já existe: {u['email']}")
    db.session.commit()

    # Referências rápidas para uso na criação de ocorrências
    ana      = usuarios['ana.lima@sirae.com.br']
    carlos   = usuarios['carlos.m@sirae.com.br']
    patricia = usuarios['patricia@sirae.com.br']
    fernanda = usuarios['fernanda.p@sirae.com.br']
    rodrigo  = usuarios['rodrigo.b@sirae.com.br']
    marcos   = usuarios['marcos.r@sirae.com.br']
    juliana  = usuarios['juliana.c@sirae.com.br']

    # ─────────────────────────────────────────
    # Inclui alunos dos níveis técnico, graduação e pós-graduação.
    # Menores de 18 anos possuem dados de responsável legal obrigatório.
    # ─────────────────────────────────────────
    alunos_data = [
        # ── TÉCNICO ──────────────────────────────────
        dict(nome='Beatriz Moraes Alves',       matricula='2026-T001', curso='Técnico em Mecatrônica', nivel='tecnico',
             serie='1º semestre', turma='A', turno='manhã',
             data_nascimento='2009-03-15', cpf='111.222.333-44',
             responsavel_nome='Sônia Alves', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99101-0001', responsavel_email='sonia.alves@email.com'),

        dict(nome='Gabriel Henrique Campos',    matricula='2026-T002', curso='Técnico em Eletroeletrônica', nivel='tecnico',
             serie='1º semestre', turma='A', turno='manhã',
             data_nascimento='2009-07-22', cpf='222.333.444-55',
             responsavel_nome='Roberto Campos', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99202-0002'),

        dict(nome='Larissa Pinto Cavalcanti',   matricula='2026-T003', curso='Técnico em Mecatrônica', nivel='tecnico',
             serie='2º semestre', turma='B', turno='tarde',
             data_nascimento='2009-11-08', cpf='333.444.555-66',
             responsavel_nome='Fátima Cavalcanti', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99303-0003', responsavel_email='fatima.cav@email.com'),

        dict(nome='Mateus Oliveira Brandão',    matricula='2026-T004', curso='Técnico em Fabricação Mecânica', nivel='tecnico',
             serie='2º semestre', turma='B', turno='tarde',
             data_nascimento='2010-04-30', cpf='444.555.666-77',
             responsavel_nome='Denise Brandão', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99404-0004'),

        dict(nome='Fernanda Castro Duarte',     matricula='2026-T005', curso='Técnico em Eletroeletrônica', nivel='tecnico',
             serie='3º semestre', turma='A', turno='manhã',
             data_nascimento='2008-09-14', cpf='555.666.777-88',
             responsavel_nome='Cláudio Duarte', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99505-0005', responsavel_email='claudio.duarte@email.com'),

        dict(nome='Vinícius Torres Magalhães',  matricula='2026-T006', curso='Técnico em Mecatrônica', nivel='tecnico',
             serie='3º semestre', turma='A', turno='noite',
             data_nascimento='2009-01-19', cpf='666.777.888-99',
             responsavel_nome='Rosana Magalhães', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99606-0006'),

        dict(nome='Isabela Nunes Figueiredo',   matricula='2026-T007', curso='Técnico em Administração', nivel='tecnico',
             serie='4º semestre', turma='C', turno='noite',
             data_nascimento='2008-06-25', cpf='777.888.999-00',
             responsavel_nome='Eduardo Figueiredo', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99707-0007', responsavel_email='edu.fig@email.com'),

        dict(nome='Rodrigo Sampaio Correia',    matricula='2026-T008', curso='Técnico em Fabricação Mecânica', nivel='tecnico',
             serie='4º semestre', turma='C', turno='noite',
             data_nascimento='2008-12-03', cpf='888.999.000-11',
             responsavel_nome='Vera Correia', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99808-0008'),

        # ── GRADUAÇÃO ─────────────────────────────────
        dict(nome='Amanda Ferreira Queiroz',    matricula='2026-G001', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='1º semestre', turma='A', turno='manhã',
             data_nascimento='2007-02-17', cpf='999.000.111-22',
             responsavel_nome='Antônio Queiroz', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99909-0009', responsavel_email='antonio.q@email.com'),

        dict(nome='Lucas Barbosa Teixeira',     matricula='2026-G002', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='1º semestre', turma='A', turno='manhã',
             data_nascimento='2007-08-11', cpf='000.111.222-33',
             responsavel_nome='Simone Teixeira', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99010-0010'),

        dict(nome='Camila Rocha Guimarães',     matricula='2026-G003', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='2º semestre', turma='B', turno='noite',
             data_nascimento='2006-05-29', cpf='111.222.333-00',
             responsavel_nome='Nelson Guimarães', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99111-0011', responsavel_email='nelson.g@email.com'),

        dict(nome='Pedro Augusto Rezende',      matricula='2026-G004', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='3º semestre', turma='A', turno='manhã',
             data_nascimento='2005-10-07', cpf='222.333.444-11',
             responsavel_nome='Cristina Rezende', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99212-0012'),

        dict(nome='Natália Vasconcelos Lima',   matricula='2026-G005', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='3º semestre', turma='B', turno='tarde',
             data_nascimento='2005-03-21', cpf='333.444.555-22',
             responsavel_nome='Márcio Lima', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99313-0013', responsavel_email='marcio.lima@email.com'),

        dict(nome='Thiago Mendonça Pereira',    matricula='2026-G006', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='4º semestre', turma='B', turno='noite',
             data_nascimento='2004-07-16', cpf='444.555.666-33',
             responsavel_nome='Lúcia Pereira', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99414-0014'),

        dict(nome='Bruna Monteiro Cardoso',     matricula='2026-G007', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='5º semestre', turma='A', turno='manhã',
             data_nascimento='2004-11-30', cpf='555.666.777-44',
             responsavel_nome='Rogério Cardoso', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99515-0015', responsavel_email='rogerio.c@email.com'),

        dict(nome='Diego Albuquerque Freitas',  matricula='2026-G008', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='5º semestre', turma='A', turno='tarde',
             data_nascimento='2003-04-08', cpf='666.777.888-55',
             responsavel_nome='Eliane Freitas', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99616-0016'),

        dict(nome='Júlia Esteves Marinho',      matricula='2026-G009', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='6º semestre', turma='B', turno='noite',
             data_nascimento='2002-08-23', cpf='777.888.999-66',
             responsavel_nome='Flávio Marinho', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99717-0017', responsavel_email='flavio.m@email.com'),

        dict(nome='Rafael Cunha Nogueira',      matricula='2026-G010', curso='Tecnologia em Mecatrônica Industrial', nivel='graduacao',
             serie='7º semestre', turma='A', turno='manhã',
             data_nascimento='2001-01-14', cpf='888.999.000-77',
             responsavel_nome='Aparecida Nogueira', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99818-0018'),

        # ── PÓS-GRADUAÇÃO ─────────────────────────────
        dict(nome='Mariana Costa Drummond',     matricula='2026-P001', curso='Pós-Graduação em Indústria Digital', nivel='pos',
             serie='1º semestre', turma='A', turno='noite',
             data_nascimento='2001-12-05', cpf='123.456.789-00',
             responsavel_nome='Paulo Drummond', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99919-0019', responsavel_email='paulo.drum@email.com'),

        dict(nome='Felipe Andrade Mota',        matricula='2026-P002', curso='Pós-Graduação em Automação da Manufatura', nivel='pos',
             serie='1º semestre', turma='B', turno='noite',
             data_nascimento='2006-05-18', cpf='987.654.321-00',
             responsavel_nome='Sandra Mota', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99020-0020'),

        # ── ALUNOS ADICIONAIS (incluídos por Celso Augusto) ──
        dict(nome='Gustavo Henrique Almeida',   matricula='2026-T009', curso='Técnico em Informática', nivel='tecnico',
             serie='1º semestre', turma='A', turno='manhã',
             data_nascimento='2009-06-10', cpf='135.246.357-88',
             responsavel_nome='Roberto Almeida', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99121-0021', responsavel_email='roberto.alm@email.com'),

        dict(nome='Carolina Ferreira Santos',   matricula='2026-T010', curso='Técnico em Logística', nivel='tecnico',
             serie='2º semestre', turma='B', turno='tarde',
             data_nascimento='2008-11-22', cpf='246.357.468-99',
             responsavel_nome='Ana Santos', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99232-0022'),
    ]

    alunos = []
    print("\n── ALUNOS ───────────────────────────────")
    for a in alunos_data:
        # Verifica se o aluno já existe antes de inserir
        ex = Aluno.query.filter_by(matricula=a['matricula']).first()
        if not ex:
            dn = datetime.strptime(a.pop('data_nascimento'), '%Y-%m-%d').date()
            novo = Aluno(data_nascimento=dn, **a)
            db.session.add(novo)
            alunos.append(novo)
            nivel_label = {'tecnico': 'Técnico', 'graduacao': 'Graduação', 'pos': 'Pós'}.get(novo.nivel, novo.nivel)
            print(f"  ✓ {novo.nome:<32} {nivel_label} · {novo.serie} · {novo.turno}")
        else:
            alunos.append(ex)
            print(f"  — Já existe: {a['nome']}")
    db.session.commit()

    # ─────────────────────────────────────────
    # OCORRÊNCIAS
    # Cobre os três estados possíveis: encerrada, em_andamento e aberta.
    # Cada ocorrência possui um histórico de logs de auditoria.
    # ─────────────────────────────────────────
    def dp(dias):
        """Retorna datetime relativo à data atual, subtraindo os dias informados."""
        return datetime.now(timezone.utc) - timedelta(days=dias)

    def criar(aluno, tipo, status, criado, responsavel, descricao, data_criacao, logs, data_enc=None):
        """
        Cria uma ocorrência com seu histórico de logs de auditoria.

        Args:
            aluno: Instância do aluno relacionado
            tipo: Tipo da ocorrência (Disciplinar, Saúde, Financeiro, etc.)
            status: Estado inicial (aberta, em_andamento, encerrada)
            criado: Usuário que criou a ocorrência
            responsavel: Usuário responsável atual
            descricao: Descrição detalhada
            data_criacao: Data e hora de criação
            logs: Lista de tuplas (acao, usuario, descricao, dias_atras)
            data_enc: Data de encerramento (opcional)
        """
        o = Ocorrencia(
            aluno_id=aluno.id, tipo=tipo, status=status,
            criado_por_id=criado.id, responsavel_id=responsavel.id,
            descricao=descricao, data_criacao=data_criacao,
            data_encerramento=data_enc
        )
        db.session.add(o)
        db.session.flush()
        for acao, usuario, desc, dias in logs:
            db.session.add(LogAuditoria(
                ocorrencia_id=o.id, usuario_id=usuario.id,
                acao=acao, descricao_acao=desc,
                data_hora=datetime.now(timezone.utc) - timedelta(days=dias)
            ))
        return o

    ocorrencias = [

        # ── ENCERRADAS ──────────────────────────────────────────────────
        criar(alunos[1], 'Disciplinar', 'encerrada', ana, marcos,
              'Aluno envolveu-se em discussão com colega durante aula prática de laboratório. Comportamento agressivo relatado pelo professor responsável.',
              dp(22), [
                  ('criada',     ana,    'Ocorrência criada por Ana Lima', 22),
                  ('encaminhada',ana,    'Encaminhada de Ana Lima para Marcos Ribeiro (coordenacao).\nMotivo: Situação requer análise da coordenação.', 21),
                  ('atualizada', marcos, 'Andamento registrado por Marcos Ribeiro: Conversa realizada com o aluno. Responsável convocado para reunião.', 18),
                  ('encerrada',  marcos, 'Encerrada por Marcos Ribeiro.\nResolução: Reunião realizada. Acordo de comportamento firmado. Aluno ciente das normas do curso.', 15),
              ], dp(15)),

        criar(alunos[4], 'Saúde', 'encerrada', carlos, juliana,
              'Aluna relatou crise de ansiedade durante prova prática. Relatou insônia e dificuldade de concentração nas últimas semanas.',
              dp(18), [
                  ('criada',     carlos,  'Ocorrência criada por Carlos Menezes', 18),
                  ('encaminhada',carlos,  'Encaminhada de Carlos Menezes para Juliana Cardoso (coordenacao).\nMotivo: Saúde mental requer acompanhamento especializado.', 17),
                  ('encerrada',  juliana, 'Encerrada por Juliana Cardoso.\nResolução: Aluna encaminhada para psicólogo parceiro da instituição.', 14),
              ], dp(14)),

        criar(alunos[11], 'Financeiro', 'encerrada', patricia, marcos,
              'Aluno com mensalidades em atraso há 2 meses. Relatou dificuldades financeiras após desemprego do responsável financeiro da família.',
              dp(30), [
                  ('criada',     patricia, 'Ocorrência criada por Patrícia Souza', 30),
                  ('encaminhada',patricia, 'Encaminhada de Patrícia Souza para Marcos Ribeiro (coordenacao).\nMotivo: Necessita análise para programa de bolsa/auxílio.', 29),
                  ('atualizada', marcos,   'Andamento registrado por Marcos Ribeiro: Família encaminhada ao setor financeiro.', 25),
                  ('encerrada',  marcos,   'Encerrada por Marcos Ribeiro.\nResolução: Aluno incluído no programa de bolsa social.', 22),
              ], dp(22)),

        criar(alunos[8], 'Evasão', 'encerrada', fernanda, juliana,
              'Aluna com 6 faltas consecutivas sem justificativa no 1º semestre.',
              dp(25), [
                  ('criada',     fernanda, 'Ocorrência criada por Fernanda Prado', 25),
                  ('encaminhada',fernanda, 'Encaminhada de Fernanda Prado para Juliana Cardoso (coordenacao).\nMotivo: Risco de evasão — intervenção urgente necessária.', 24),
                  ('atualizada', juliana,  'Andamento registrado por Juliana Cardoso: Contato realizado com a aluna por telefone.', 20),
                  ('encerrada',  juliana,  'Encerrada por Juliana Cardoso.\nResolução: Plano de acompanhamento montado. Aluna retornou às aulas.', 18),
              ], dp(18)),

        # ── EM ANDAMENTO ────────────────────────────────────────────────
        criar(alunos[6], 'Psicossocial', 'em_andamento', ana, marcos,
              'Aluna demonstra sinais de sofrimento emocional — isolamento social, choro frequente em sala e relatos de conflitos familiares sérios.',
              dp(10), [
                  ('criada',     ana,    'Ocorrência criada por Ana Lima', 10),
                  ('encaminhada',ana,    'Encaminhada de Ana Lima para Marcos Ribeiro (coordenacao).', 9),
                  ('atualizada', marcos, 'Andamento registrado por Marcos Ribeiro: Aluna encaminhada para psicólogo parceiro.', 6),
              ]),

        criar(alunos[12], 'Acadêmico', 'em_andamento', carlos, fernanda,
              'Aluno com queda brusca de rendimento no 3º semestre. Média geral caiu de 7,8 para 4,2.',
              dp(7), [
                  ('criada',     carlos,   'Ocorrência criada por Carlos Menezes', 7),
                  ('encaminhada',carlos,   'Encaminhada de Carlos Menezes para Fernanda Prado (pedagogia).', 6),
                  ('atualizada', fernanda, 'Andamento registrado por Fernanda Prado: Monitor de reforço indicado.', 4),
                  ('atualizada', fernanda, 'Andamento registrado por Fernanda Prado: Aluno iniciou reforço com monitor.', 2),
              ]),

        criar(alunos[9], 'Evasão', 'em_andamento', patricia, rodrigo,
              'Aluno do 1º semestre com histórico de 4 faltas na última semana. Relatou pensamentos de desistência.',
              dp(8), [
                  ('criada',     patricia, 'Ocorrência criada por Patrícia Souza', 8),
                  ('encaminhada',patricia, 'Encaminhada de Patrícia Souza para Rodrigo Bastos (pedagogia).', 7),
                  ('atualizada', rodrigo,  'Andamento registrado por Rodrigo Bastos: Plano de apoio montado.', 5),
              ]),

        criar(alunos[18], 'Psicossocial', 'em_andamento', ana, marcos,
              'Aluna do 8º semestre relatou síndrome de burnout — exaustão intensa, próxima ao TCC.',
              dp(5), [
                  ('criada',     ana,    'Ocorrência criada por Ana Lima', 5),
                  ('encaminhada',ana,    'Encaminhada de Ana Lima para Marcos Ribeiro (coordenacao).', 4),
                  ('atualizada', marcos, 'Andamento registrado por Marcos Ribeiro: Prazo de entrega do TCC negociado.', 2),
              ]),

        # ── ABERTAS ─────────────────────────────────────────────────────
        criar(alunos[0], 'Acadêmico', 'aberta', ana, ana,
              'Aluna do 1º semestre com dificuldades em eletricidade básica.',
              dp(2), [('criada', ana, 'Ocorrência criada por Ana Lima', 2)]),

        criar(alunos[13], 'Disciplinar', 'aberta', carlos, carlos,
              'Aluno flagrado utilizando celular durante avaliação, configurando possível cola.',
              dp(1), [('criada', carlos, 'Ocorrência criada por Carlos Menezes', 1)]),

        criar(alunos[2], 'Financeiro', 'aberta', patricia, patricia,
              'Aluna solicitou informações sobre bolsas e programas de auxílio financeiro.',
              dp(1), [('criada', patricia, 'Ocorrência criada por Patrícia Souza', 1)]),

        criar(alunos[16], 'Evasão', 'aberta', ana, ana,
              'Aluno com frequência abaixo de 75% em 3 disciplinas. Não respondeu aos contatos anteriores.',
              dp(0), [('criada', ana, 'Ocorrência criada por Ana Lima', 0)]),

        criar(alunos[19], 'Psicossocial', 'aberta', carlos, carlos,
              'Aluno relatou dificuldades de relacionamento no ambiente de trabalho durante estágio obrigatório.',
              dp(0), [('criada', carlos, 'Ocorrência criada por Carlos Menezes', 0)]),

        # Segunda ocorrência do Gabriel (reincidente)
        criar(alunos[1], 'Disciplinar', 'aberta', patricia, patricia,
              'Segunda ocorrência disciplinar do aluno no semestre. Desrespeito verbal ao colega de turma.',
              dp(3), [('criada', patricia, 'Ocorrência criada por Patrícia Souza', 3)]),
    ]

    db.session.commit()

    # ─────────────────────────────────────────
    # RESUMO FINAL
    # ─────────────────────────────────────────
    print(f"\n── RESUMO ───────────────────────────────")
    enc  = sum(1 for o in ocorrencias if o.status == 'encerrada')
    and_ = sum(1 for o in ocorrencias if o.status == 'em_andamento')
    ab   = sum(1 for o in ocorrencias if o.status == 'aberta')
    tec  = sum(1 for a in alunos_data if a.get('nivel') == 'tecnico')
    grad = sum(1 for a in alunos_data if a.get('nivel') == 'graduacao')
    print(f"  Usuários    : {len(usuarios_data)}")
    print(f"  Alunos      : {len(alunos_data)} ({tec} técnico · {grad} graduação)")
    print(f"  Ocorrências : {len(ocorrencias)} ({enc} encerradas · {and_} em andamento · {ab} abertas)")
    print("\n" + "="*50)
    print("✓ Seed concluído!")
    print("="*50)
    print("\nCredenciais:")
    print("  admin@sirae.com.br       / admin123  → Administrador")
    print("  ana.lima@sirae.com.br    / 123456    → Atendente")
    print("  carlos.m@sirae.com.br    / 123456    → Atendente")
    print("  patricia@sirae.com.br    / 123456    → Atendente")
    print("  fernanda.p@sirae.com.br  / 123456    → Pedagogo")
    print("  rodrigo.b@sirae.com.br   / 123456    → Pedagogo")
    print("  marcos.r@sirae.com.br    / 123456    → Coordenação")
    print("  juliana.c@sirae.com.br   / 123456    → Coordenação")
    print("\nAcesse: http://localhost:5000")
