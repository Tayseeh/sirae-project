"""
seed.py — Script de carga inicial de dados do SIRAE
Autor: Celso Augusto Cândido Cacholi
Função: Banco de Dados e Modelagem

Descrição:
    Cria todas as tabelas no banco e popula com dados fictícios realistas
    baseados nos cursos reais do SENAI Antônio Adolpho Lobbe (São Carlos/SP).
    Os níveis disponíveis são: aprendizagem, tecnico, graduacao, pos, livre.
    O campo turma só é utilizado para a Aprendizagem Industrial.

Execução:
    python seed.py

Pré-requisitos:
    - Banco de dados criado conforme README.md
    - Arquivo .env configurado com DATABASE_URL
"""

from app import create_app, db
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from app.models.ocorrencia import Ocorrencia, LogAuditoria
from app.models.log_admin import LogAdmin
from app.models.notificacao import Notificacao
from datetime import datetime, timedelta, timezone

BRASILIA = timezone(timedelta(hours=-3))

app = create_app()

with app.app_context():
    db.create_all()

    # ── USUÁRIOS ─────────────────────────────────────────────────────────────
    usuarios_data = [
        dict(email='admin@sirae.com.br',      nome='Administrador',          perfil='admin',
             cargo='Analista de TI',          telefone='(16) 3301-1000', ramal='2000', senha='admin123'),
        dict(email='ana.lima@sirae.com.br',   nome='Ana Lima',               perfil='atendente',
             cargo='Atendente do Setor de Apoio', telefone='(16) 99101-1111', ramal='2011', senha='123456'),
        dict(email='carlos.m@sirae.com.br',   nome='Carlos Menezes',         perfil='atendente',
             cargo='Assistente Estudantil',   telefone='(16) 99202-2222', ramal='2012', senha='123456'),
        dict(email='patricia@sirae.com.br',   nome='Patrícia Souza',         perfil='atendente',
             cargo='Atendente do Setor de Apoio', telefone='(16) 99303-3333', ramal='2013', senha='123456'),
        dict(email='fernanda.p@sirae.com.br', nome='Fernanda Prado',         perfil='pedagogia',
             cargo='Pedagoga',                telefone='(16) 99404-4444', ramal='2021', senha='123456'),
        dict(email='rodrigo.b@sirae.com.br',  nome='Rodrigo Bastos',         perfil='pedagogia',
             cargo='Pedagogo',                telefone='(16) 99505-5555', ramal='2022', senha='123456'),
        dict(email='marcos.r@sirae.com.br',   nome='Marcos Ribeiro',         perfil='coordenacao',
             cargo='Coordenador Pedagógico',  telefone='(16) 99606-6666', ramal='2031', senha='123456'),
        dict(email='juliana.c@sirae.com.br',  nome='Juliana Cardoso',        perfil='coordenacao',
             cargo='Coordenadora de Apoio',   telefone='(16) 99707-7777', ramal='2032', senha='123456'),
    ]

    usuarios = {}
    print("\n── USUÁRIOS ─────────────────────────────────────────────────────")
    for u in usuarios_data:
        ex = Usuario.query.filter_by(email=u['email']).first()
        if not ex:
            novo = Usuario(email=u['email'], nome=u['nome'], perfil=u['perfil'],
                           cargo=u['cargo'], telefone=u['telefone'], ramal=u['ramal'])
            novo.set_password(u['senha'])
            db.session.add(novo)
            db.session.flush()
            usuarios[u['email']] = novo
            print(f"  ✓ {u['nome']:<30} [{u['perfil']:<12}] ramal {u['ramal']}")
        else:
            usuarios[u['email']] = ex
            print(f"  — Já existe: {u['email']}")
    db.session.commit()

    ana      = usuarios['ana.lima@sirae.com.br']
    carlos   = usuarios['carlos.m@sirae.com.br']
    patricia = usuarios['patricia@sirae.com.br']
    fernanda = usuarios['fernanda.p@sirae.com.br']
    rodrigo  = usuarios['rodrigo.b@sirae.com.br']
    marcos   = usuarios['marcos.r@sirae.com.br']
    juliana  = usuarios['juliana.c@sirae.com.br']

    # ── ALUNOS ───────────────────────────────────────────────────────────────
    # Turma só existe para Aprendizagem Industrial.
    # Formato: AI-[turno inicial][letra] — ex: AI-MA = Manhã turma A
    alunos_data = [

        # ── APRENDIZAGEM INDUSTRIAL ──────────────────────────────────────────
        dict(nome='Beatriz Moraes Alves',       matricula='2026AI001',
             nivel='aprendizagem', curso='Aprendizagem em Mecatrônica',
             serie='1º ano', turma='AI-MA', turno='manhã',
             data_nascimento='2009-03-15', cpf='111.222.333-44',
             tipo_contato='responsavel',
             responsavel_nome='Sônia Alves', responsavel_parentesco='Mãe',
             responsavel_cpf='555.666.777-88',
             responsavel_contato='(16) 99101-0001', responsavel_email='sonia.alves@email.com'),

        dict(nome='Gabriel Henrique Campos',    matricula='2026AI002',
             nivel='aprendizagem', curso='Aprendizagem em Eletroeletrônica',
             serie='1º ano', turma='AI-MA', turno='manhã',
             data_nascimento='2009-07-22', cpf='222.333.444-55',
             tipo_contato='responsavel',
             responsavel_nome='Roberto Campos', responsavel_parentesco='Pai',
             responsavel_cpf='666.777.888-99',
             responsavel_contato='(16) 99202-0002'),

        dict(nome='Larissa Pinto Cavalcanti',   matricula='2026AI003',
             nivel='aprendizagem', curso='Aprendizagem em Fabricação Mecânica',
             serie='1º ano', turma='AI-TA', turno='tarde',
             data_nascimento='2009-11-08', cpf='333.444.555-66',
             tipo_contato='responsavel',
             responsavel_nome='Fátima Cavalcanti', responsavel_parentesco='Mãe',
             responsavel_cpf='777.888.999-00',
             responsavel_contato='(16) 99303-0003', responsavel_email='fatima.cav@email.com'),

        dict(nome='Mateus Oliveira Brandão',    matricula='2026AI004',
             nivel='aprendizagem', curso='Aprendizagem em Logística',
             serie='1º ano', turma='AI-TA', turno='tarde',
             data_nascimento='2010-04-30', cpf='444.555.666-77',
             tipo_contato='responsavel',
             responsavel_nome='Denise Brandão', responsavel_parentesco='Mãe',
             responsavel_cpf='888.999.000-11',
             responsavel_contato='(16) 99404-0004'),

        dict(nome='Fernanda Castro Duarte',     matricula='2026AI005',
             nivel='aprendizagem', curso='Aprendizagem em Administração',
             serie='2º ano', turma='AI-MB', turno='manhã',
             data_nascimento='2008-09-14', cpf='555.666.777-88',
             tipo_contato='responsavel',
             responsavel_nome='Cláudio Duarte', responsavel_parentesco='Pai',
             responsavel_cpf='999.000.111-22',
             responsavel_contato='(16) 99505-0005', responsavel_email='claudio.duarte@email.com'),

        dict(nome='Vinícius Torres Magalhães',  matricula='2026AI006',
             nivel='aprendizagem', curso='Aprendizagem em Tecnologia da Informação',
             serie='2º ano', turma='AI-NB', turno='noite',
             data_nascimento='2009-01-19', cpf='666.777.888-99',
             tipo_contato='responsavel',
             responsavel_nome='Rosana Magalhães', responsavel_parentesco='Mãe',
             responsavel_cpf='000.111.222-33',
             responsavel_contato='(16) 99606-0006'),

        dict(nome='Isabela Nunes Figueiredo',   matricula='2026AI007',
             nivel='aprendizagem', curso='Aprendizagem em Soldagem',
             serie='2º ano', turma='AI-TB', turno='tarde',
             data_nascimento='2008-06-25', cpf='777.888.999-00',
             tipo_contato='responsavel',
             responsavel_nome='Eduardo Figueiredo', responsavel_parentesco='Pai',
             responsavel_cpf='111.222.333-44',
             responsavel_contato='(16) 99707-0007', responsavel_email='edu.fig@email.com'),

        dict(nome='Rodrigo Sampaio Correia',    matricula='2026AI008',
             nivel='aprendizagem', curso='Aprendizagem em Automotiva',
             serie='1º ano', turma='AI-NA', turno='noite',
             data_nascimento='2008-12-03', cpf='888.999.000-11',
             tipo_contato='responsavel',
             responsavel_nome='Vera Correia', responsavel_parentesco='Mãe',
             responsavel_cpf='222.333.444-55',
             responsavel_contato='(16) 99808-0008'),

        # ── TÉCNICO ──────────────────────────────────────────────────────────
        dict(nome='Amanda Ferreira Queiroz',    matricula='2026T001',
             nivel='tecnico', curso='Técnico em Mecatrônica',
             serie='1º semestre', turno='manhã',
             data_nascimento='2007-02-17', cpf='999.000.111-22',
             tipo_contato='responsavel',
             responsavel_nome='Antônio Queiroz', responsavel_parentesco='Pai',
             responsavel_cpf='333.444.555-66',
             responsavel_contato='(16) 99909-0009', responsavel_email='antonio.q@email.com'),

        dict(nome='Lucas Barbosa Teixeira',     matricula='2026T002',
             nivel='tecnico', curso='Técnico em Eletroeletrônica',
             serie='2º semestre', turno='manhã',
             data_nascimento='2007-08-11', cpf='000.111.222-33',
             tipo_contato='responsavel',
             responsavel_nome='Simone Teixeira', responsavel_parentesco='Mãe',
             responsavel_cpf='444.555.666-77',
             responsavel_contato='(16) 99010-0010'),

        dict(nome='Camila Rocha Guimarães',     matricula='2025T031',
             nivel='tecnico', curso='Técnico em Fabricação Mecânica',
             serie='3º semestre', turno='noite',
             data_nascimento='2006-05-29', cpf='111.222.333-00',
             email='camila.guim@email.com', telefone='(16) 99111-0011',
             tipo_contato='emergencia',
             responsavel_nome='Nelson Guimarães', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99111-0012'),

        dict(nome='Pedro Augusto Rezende',      matricula='2025T032',
             nivel='tecnico', curso='Técnico em Logística',
             serie='3º semestre', turno='manhã',
             data_nascimento='2005-10-07', cpf='222.333.444-11',
             email='pedro.rezende@email.com', telefone='(16) 99212-0012',
             tipo_contato='emergencia',
             responsavel_nome='Cristina Rezende', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99212-0013'),

        dict(nome='Natália Vasconcelos Lima',   matricula='2025T033',
             nivel='tecnico', curso='Técnico em Tecnologia da Informação',
             serie='4º semestre', turno='tarde',
             data_nascimento='2005-03-21', cpf='333.444.555-22',
             email='natalia.lima@email.com', telefone='(16) 99313-0013',
             tipo_contato='emergencia',
             responsavel_nome='Márcio Lima', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99313-0014', responsavel_email='marcio.lima@email.com'),

        dict(nome='Thiago Mendonça Pereira',    matricula='2025T034',
             nivel='tecnico', curso='Técnico em Soldagem',
             serie='4º semestre', turno='noite',
             data_nascimento='2004-07-16', cpf='444.555.666-33',
             email='thiago.pereira@email.com', telefone='(16) 99414-0014',
             tipo_contato='emergencia',
             responsavel_nome='Lúcia Pereira', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99414-0015'),

        dict(nome='Bruna Monteiro Cardoso',     matricula='2025T035',
             nivel='tecnico', curso='Técnico em Administração',
             serie='3º semestre', turno='manhã',
             data_nascimento='2004-11-30', cpf='555.666.777-44',
             email='bruna.cardoso@email.com', telefone='(16) 99515-0015',
             tipo_contato='emergencia',
             responsavel_nome='Rogério Cardoso', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99515-0016', responsavel_email='rogerio.c@email.com'),

        dict(nome='Diego Albuquerque Freitas',  matricula='2025T036',
             nivel='tecnico', curso='Técnico em Automotiva',
             serie='2º semestre', turno='tarde',
             data_nascimento='2003-04-08', cpf='666.777.888-55',
             email='diego.freitas@email.com', telefone='(16) 99616-0016',
             tipo_contato='emergencia',
             responsavel_nome='Eliane Freitas', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99616-0017'),

        # ── GRADUAÇÃO ─────────────────────────────────────────────────────────
        dict(nome='Júlia Esteves Marinho',      matricula='2024G001',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='5º semestre', turno='noite',
             data_nascimento='2002-08-23', cpf='777.888.999-66',
             email='julia.marinho@email.com', telefone='(16) 99717-0017',
             tipo_contato='emergencia',
             responsavel_nome='Flávio Marinho', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99717-0018', responsavel_email='flavio.m@email.com'),

        dict(nome='Rafael Cunha Nogueira',      matricula='2024G002',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='5º semestre', turno='noite',
             data_nascimento='2001-01-14', cpf='888.999.000-77',
             email='rafael.nogueira@email.com', telefone='(16) 99818-0018',
             tipo_contato='emergencia',
             responsavel_nome='Aparecida Nogueira', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99818-0019'),

        dict(nome='Mariana Costa Drummond',     matricula='2023G015',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='7º semestre', turno='noite',
             data_nascimento='2001-12-05', cpf='123.456.789-00',
             email='mariana.drummond@email.com', telefone='(16) 99919-0019',
             tipo_contato='emergencia',
             responsavel_nome='Paulo Drummond', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99919-0020', responsavel_email='paulo.drum@email.com'),

        # ── PÓS-GRADUAÇÃO ─────────────────────────────────────────────────────
        dict(nome='Felipe Andrade Mota',        matricula='2025PG001',
             nivel='pos', curso='Pós-Graduação em Indústria Digital',
             serie='1º semestre', turno='noite',
             data_nascimento='1998-05-18', cpf='987.654.321-00',
             email='felipe.mota@email.com', telefone='(16) 99020-0020',
             tipo_contato='emergencia',
             responsavel_nome='Sandra Mota', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99020-0021'),

        dict(nome='Renata Oliveira Santana',    matricula='2025PG002',
             nivel='pos', curso='Pós-Graduação em Automação da Manufatura',
             serie='2º semestre', turno='noite',
             data_nascimento='1995-09-30', cpf='135.246.357-11',
             email='renata.santana@email.com', telefone='(16) 99121-0021',
             tipo_contato='emergencia',
             responsavel_nome='Carlos Santana', responsavel_parentesco='Cônjuge',
             responsavel_contato='(16) 99121-0022', responsavel_email='carlos.san@email.com'),

        # ── FORMAÇÃO CONTINUADA ───────────────────────────────────────────────
        dict(nome='Gustavo Henrique Almeida',   matricula='2026FC001',
             nivel='livre', curso='NR-10 Básico',
             turno='manhã',
             data_nascimento='1992-06-10', cpf='246.357.468-22',
             email='gustavo.almeida@email.com', telefone='(16) 99232-0022',
             tipo_contato='emergencia',
             responsavel_nome='Carla Almeida', responsavel_parentesco='Cônjuge',
             responsavel_contato='(16) 99232-0023'),

        dict(nome='Carolina Ferreira Santos',   matricula='2026FC002',
             nivel='livre', curso='Programação CNC',
             turno='tarde',
             data_nascimento='1990-11-22', cpf='357.468.579-33',
             email='carolina.santos@email.com', telefone='(16) 99343-0023',
             tipo_contato='emergencia',
             responsavel_nome='João Santos', responsavel_parentesco='Cônjuge',
             responsavel_contato='(16) 99343-0024'),
    ]

    alunos = []
    print("\n── ALUNOS ───────────────────────────────────────────────────────")
    niveis_label = {
        'aprendizagem': 'Aprendizagem',
        'tecnico': 'Técnico',
        'graduacao': 'Graduação',
        'pos': 'Pós',
        'livre': 'Livre'
    }
    for a in alunos_data:
        ex = Aluno.query.filter_by(matricula=a['matricula']).first()
        if not ex:
            dn_str = a.pop('data_nascimento', None)
            from datetime import date
            dn = datetime.strptime(dn_str, '%Y-%m-%d').date() if dn_str else None
            novo = Aluno(data_nascimento=dn, **a)
            db.session.add(novo)
            alunos.append(novo)
            label = niveis_label.get(novo.nivel, novo.nivel)
            turma = f' · {novo.turma}' if novo.turma else ''
            print(f"  ✓ {novo.nome:<32} {label}{turma} · {novo.turno or '-'}")
        else:
            alunos.append(ex)
            print(f"  — Já existe: {a['nome']}")
    db.session.commit()

    # ── OCORRÊNCIAS ──────────────────────────────────────────────────────────
    def dp(dias):
        return datetime.now(BRASILIA) - timedelta(days=dias)

    def criar(aluno, tipo, status, criado, responsavel, descricao, data_criacao, logs, data_enc=None):
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
                data_hora=datetime.now(BRASILIA) - timedelta(days=dias)
            ))
        return o

    ocorrencias = [
        # Encerradas
        criar(alunos[1], 'Disciplinar', 'encerrada', ana, marcos,
              'Aluno envolveu-se em discussão com colega durante aula prática de laboratório.',
              dp(22), [
                  ('criada',     ana,    'Ocorrência criada por Ana Lima.', 22),
                  ('encaminhada',ana,    'Encaminhada para Marcos Ribeiro (coordenacao). Motivo: Requer análise da coordenação.', 21),
                  ('atualizada', marcos, 'Conversa realizada com o aluno. Responsável convocado para reunião.', 18),
                  ('encerrada',  marcos, 'Resolução: Reunião realizada. Acordo de comportamento firmado.', 15),
              ], dp(15)),

        criar(alunos[4], 'Saúde', 'encerrada', carlos, juliana,
              'Aluna relatou crise de ansiedade durante prova prática. Insônia e dificuldade de concentração.',
              dp(18), [
                  ('criada',     carlos,  'Ocorrência criada por Carlos Menezes.', 18),
                  ('encaminhada',carlos,  'Encaminhada para Juliana Cardoso (coordenacao). Motivo: Saúde mental requer acompanhamento.', 17),
                  ('encerrada',  juliana, 'Resolução: Aluna encaminhada para psicólogo parceiro da instituição.', 14),
              ], dp(14)),

        criar(alunos[10], 'Financeiro', 'encerrada', patricia, marcos,
              'Aluno com mensalidades em atraso. Dificuldades financeiras após desemprego do responsável.',
              dp(30), [
                  ('criada',     patricia, 'Ocorrência criada por Patrícia Souza.', 30),
                  ('encaminhada',patricia, 'Encaminhada para Marcos Ribeiro. Motivo: Necessita análise para programa de bolsa.', 29),
                  ('atualizada', marcos,   'Família encaminhada ao setor financeiro.', 25),
                  ('encerrada',  marcos,   'Resolução: Aluno incluído no programa de bolsa social.', 22),
              ], dp(22)),

        criar(alunos[8], 'Evasão', 'encerrada', fernanda, juliana,
              'Aluno com 6 faltas consecutivas sem justificativa no 1º semestre.',
              dp(25), [
                  ('criada',     fernanda, 'Ocorrência criada por Fernanda Prado.', 25),
                  ('encaminhada',fernanda, 'Encaminhada para Juliana Cardoso. Motivo: Risco de evasão.', 24),
                  ('atualizada', juliana,  'Contato realizado com o aluno por telefone.', 20),
                  ('encerrada',  juliana,  'Resolução: Plano de acompanhamento montado. Aluno retornou às aulas.', 18),
              ], dp(18)),

        # Em andamento
        criar(alunos[6], 'Psicossocial', 'em_andamento', ana, marcos,
              'Aluna demonstra sinais de sofrimento emocional — isolamento social e conflitos familiares.',
              dp(10), [
                  ('criada',     ana,    'Ocorrência criada por Ana Lima.', 10),
                  ('encaminhada',ana,    'Encaminhada para Marcos Ribeiro.', 9),
                  ('atualizada', marcos, 'Aluna encaminhada para psicólogo parceiro.', 6),
              ]),

        criar(alunos[11], 'Acadêmico', 'em_andamento', carlos, fernanda,
              'Aluno com queda brusca de rendimento no 3º semestre. Média caiu de 7,8 para 4,2.',
              dp(7), [
                  ('criada',     carlos,   'Ocorrência criada por Carlos Menezes.', 7),
                  ('encaminhada',carlos,   'Encaminhada para Fernanda Prado (pedagogia).', 6),
                  ('atualizada', fernanda, 'Monitor de reforço indicado.', 4),
                  ('atualizada', fernanda, 'Aluno iniciou reforço com monitor.', 2),
              ]),

        criar(alunos[9], 'Evasão', 'em_andamento', patricia, rodrigo,
              'Aluno com 4 faltas na última semana. Relatou pensamentos de desistência do curso.',
              dp(8), [
                  ('criada',     patricia, 'Ocorrência criada por Patrícia Souza.', 8),
                  ('encaminhada',patricia, 'Encaminhada para Rodrigo Bastos (pedagogia).', 7),
                  ('atualizada', rodrigo,  'Plano de apoio montado.', 5),
              ]),

        criar(alunos[17], 'Psicossocial', 'em_andamento', ana, marcos,
              'Aluno de pós-graduação relatou síndrome de burnout — exaustão intensa, próximo ao TCC.',
              dp(5), [
                  ('criada',     ana,    'Ocorrência criada por Ana Lima.', 5),
                  ('encaminhada',ana,    'Encaminhada para Marcos Ribeiro.', 4),
                  ('atualizada', marcos, 'Prazo de entrega do TCC negociado.', 2),
              ]),

        # Abertas
        criar(alunos[0],  'Acadêmico',    'aberta', ana,      ana,      'Aluna do 1º ano com dificuldades em eletricidade básica.',                                           dp(2), [('criada', ana,      'Ocorrência criada por Ana Lima.',      2)]),
        criar(alunos[12], 'Disciplinar',  'aberta', carlos,   carlos,   'Aluno flagrado com celular durante avaliação, possível cola.',                                        dp(1), [('criada', carlos,   'Ocorrência criada por Carlos Menezes.', 1)]),
        criar(alunos[2],  'Financeiro',   'aberta', patricia, patricia, 'Aluna solicitou informações sobre bolsas e programas de auxílio.',                                   dp(1), [('criada', patricia, 'Ocorrência criada por Patrícia Souza.', 1)]),
        criar(alunos[15], 'Evasão',       'aberta', ana,      ana,      'Aluno com frequência abaixo de 75% em 3 disciplinas. Não respondeu aos contatos.',                   dp(0), [('criada', ana,      'Ocorrência criada por Ana Lima.',      0)]),
        criar(alunos[18], 'Psicossocial', 'aberta', carlos,   carlos,   'Aluno de pós relatou dificuldades de relacionamento no ambiente de trabalho durante estágio.',       dp(0), [('criada', carlos,   'Ocorrência criada por Carlos Menezes.', 0)]),
        criar(alunos[1],  'Disciplinar',  'aberta', patricia, patricia, 'Segunda ocorrência disciplinar do aluno no semestre. Desrespeito verbal a colega de turma.',         dp(3), [('criada', patricia, 'Ocorrência criada por Patrícia Souza.', 3)]),
        criar(alunos[20], 'Acadêmico',    'aberta', ana,      ana,      'Aluno de formação continuada com dificuldade de acompanhar o ritmo do curso. Solicita nivelamento.', dp(1), [('criada', ana,      'Ocorrência criada por Ana Lima.',      1)]),
    ]

    db.session.commit()

    print(f"\n── RESUMO ───────────────────────────────────────────────────────")
    enc  = sum(1 for o in ocorrencias if o.status == 'encerrada')
    and_ = sum(1 for o in ocorrencias if o.status == 'em_andamento')
    ab   = sum(1 for o in ocorrencias if o.status == 'aberta')
    por_nivel = {}
    for a in alunos_data:
        por_nivel[a.get('nivel','?')] = por_nivel.get(a.get('nivel','?'), 0) + 1
    print(f"  Usuários    : {len(usuarios_data)}")
    print(f"  Alunos      : {len(alunos_data)}")
    for n, q in por_nivel.items():
        print(f"    {niveis_label.get(n, n):<18}: {q}")
    print(f"  Ocorrências : {len(ocorrencias)} ({enc} encerradas · {and_} em andamento · {ab} abertas)")
    print("\n" + "="*60)
    print("✓ Seed concluído!")
    print("="*60)
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
