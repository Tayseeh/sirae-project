"""
Seed completo do SIRAE — SENAI Antônio Adolpho Lobbe · São Carlos SP
Execute: python seed.py
"""
from app import create_app, db
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from app.models.ocorrencia import Ocorrencia, LogAuditoria
from datetime import datetime, timedelta, timezone

app = create_app()

def agora(dias=0):
    return datetime.now(timezone.utc) - timedelta(days=dias)

with app.app_context():
    db.create_all()

    # ─────────────────────────────────────────
    # USUÁRIOS
    # ─────────────────────────────────────────
    usuarios_data = [
        dict(email='admin@sirae.com.br',      nome='Administrador',           perfil='admin',
             cargo='Analista de TI',           telefone='(16) 3301-1000',      ramal='2000', senha='admin123'),
        dict(email='ana.lima@sirae.com.br',    nome='Ana Lima',                perfil='atendente',
             cargo='Atendente de Apoio',       telefone='(16) 99101-1111',     ramal='2011', senha='123456'),
        dict(email='carlos.m@sirae.com.br',    nome='Carlos Menezes',          perfil='atendente',
             cargo='Atendente de Apoio',       telefone='(16) 99202-2222',     ramal='2012', senha='123456'),
        dict(email='patricia@sirae.com.br',    nome='Patrícia Souza',          perfil='atendente',
             cargo='Assistente Estudantil',    telefone='(16) 99303-3333',     ramal='2013', senha='123456'),
        dict(email='fernanda.p@sirae.com.br',  nome='Fernanda Prado',          perfil='pedagogia',
             cargo='Pedagoga',                 telefone='(16) 99404-4444',     ramal='2021', senha='123456'),
        dict(email='rodrigo.b@sirae.com.br',   nome='Rodrigo Bastos',          perfil='pedagogia',
             cargo='Pedagogo',                 telefone='(16) 99505-5555',     ramal='2022', senha='123456'),
        dict(email='marcos.r@sirae.com.br',    nome='Marcos Ribeiro',          perfil='coordenacao',
             cargo='Coordenador Pedagógico',   telefone='(16) 99606-6666',     ramal='2031', senha='123456'),
        dict(email='juliana.c@sirae.com.br',   nome='Juliana Cardoso',         perfil='coordenacao',
             cargo='Coordenadora de Apoio',    telefone='(16) 99707-7777',     ramal='2032', senha='123456'),
    ]

    usuarios = {}
    print("\n── USUÁRIOS ─────────────────────────────")
    for u in usuarios_data:
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

    ana      = usuarios['ana.lima@sirae.com.br']
    carlos   = usuarios['carlos.m@sirae.com.br']
    patricia = usuarios['patricia@sirae.com.br']
    fernanda = usuarios['fernanda.p@sirae.com.br']
    rodrigo  = usuarios['rodrigo.b@sirae.com.br']
    marcos   = usuarios['marcos.r@sirae.com.br']
    juliana  = usuarios['juliana.c@sirae.com.br']

    # ─────────────────────────────────────────
    # ALUNOS — SENAI Antônio Adolpho Lobbe
    # ─────────────────────────────────────────
    alunos_data = [

        # ── TÉCNICO ──────────────────────────────────────────────────────
        dict(matricula='2026-T001', nome='Beatriz Moraes Alves',
             nivel='tecnico', curso='Técnico em Mecatrônica',
             serie='1º semestre', turma='A', turno='manhã',
             data_nascimento='2009-03-15', cpf='111.222.333-44',
             email='beatriz.alves@email.com', telefone='(16) 99101-0001',
             tipo_contato='responsavel',
             responsavel_nome='Sônia Alves', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99101-0001', responsavel_email='sonia.alves@email.com'),

        dict(matricula='2026-T002', nome='Gabriel Henrique Campos',
             nivel='tecnico', curso='Técnico em Eletroeletrônica',
             serie='1º semestre', turma='A', turno='manhã',
             data_nascimento='2009-07-22', cpf='222.333.444-55',
             email='gabriel.campos@email.com', telefone='(16) 99202-0002',
             tipo_contato='responsavel',
             responsavel_nome='Roberto Campos', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99202-0002'),

        dict(matricula='2026-T003', nome='Larissa Pinto Cavalcanti',
             nivel='tecnico', curso='Técnico em Mecatrônica',
             serie='2º semestre', turma='B', turno='tarde',
             data_nascimento='2009-11-08', cpf='333.444.555-66',
             email='larissa.cavalcanti@email.com', telefone='(16) 99303-0003',
             tipo_contato='responsavel',
             responsavel_nome='Fátima Cavalcanti', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99303-0003', responsavel_email='fatima.cav@email.com'),

        dict(matricula='2026-T004', nome='Mateus Oliveira Brandão',
             nivel='tecnico', curso='Técnico em Fabricação Mecânica',
             serie='2º semestre', turma='B', turno='tarde',
             data_nascimento='2010-04-30', cpf='444.555.666-77',
             email='mateus.brandao@email.com', telefone='(16) 99404-0004',
             tipo_contato='responsavel',
             responsavel_nome='Denise Brandão', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99404-0004'),

        dict(matricula='2026-T005', nome='Fernanda Castro Duarte',
             nivel='tecnico', curso='Técnico em Eletroeletrônica',
             serie='3º semestre', turma='A', turno='manhã',
             data_nascimento='2008-09-14', cpf='555.666.777-88',
             email='fernanda.duarte@email.com', telefone='(16) 99505-0005',
             tipo_contato='responsavel',
             responsavel_nome='Cláudio Duarte', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99505-0005', responsavel_email='claudio.duarte@email.com'),

        dict(matricula='2026-T006', nome='Vinícius Torres Magalhães',
             nivel='tecnico', curso='Técnico em Mecatrônica',
             serie='3º semestre', turma='A', turno='noite',
             data_nascimento='2009-01-19', cpf='666.777.888-99',
             email='vinicius.magalhaes@email.com', telefone='(16) 99606-0006',
             tipo_contato='responsavel',
             responsavel_nome='Rosana Magalhães', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99606-0006'),

        dict(matricula='2026-T007', nome='Isabela Nunes Figueiredo',
             nivel='tecnico', curso='Técnico em Administração',
             serie='4º semestre', turma='C', turno='noite',
             data_nascimento='2008-06-25', cpf='777.888.999-00',
             email='isabela.figueiredo@email.com', telefone='(16) 99707-0007',
             tipo_contato='responsavel',
             responsavel_nome='Eduardo Figueiredo', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99707-0007', responsavel_email='edu.fig@email.com'),

        dict(matricula='2026-T008', nome='Rodrigo Sampaio Correia',
             nivel='tecnico', curso='Técnico em Fabricação Mecânica',
             serie='4º semestre', turma='C', turno='noite',
             data_nascimento='2008-12-03', cpf='888.999.000-11',
             email='rodrigo.correia@email.com', telefone='(16) 99808-0008',
             tipo_contato='responsavel',
             responsavel_nome='Vera Correia', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99808-0008'),

        # ── GRADUAÇÃO ─────────────────────────────────────────────────────
        dict(matricula='2026-G001', nome='Amanda Ferreira Queiroz',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='1º semestre', turma='A', turno='manhã',
             data_nascimento='2007-02-17', cpf='999.000.111-22',
             email='amanda.queiroz@email.com', telefone='(16) 99909-0009',
             tipo_contato='emergencia',
             responsavel_nome='Antônio Queiroz', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99909-0009', responsavel_email='antonio.q@email.com'),

        dict(matricula='2026-G002', nome='Lucas Barbosa Teixeira',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='1º semestre', turma='A', turno='manhã',
             data_nascimento='2007-08-11', cpf='000.111.222-33',
             email='lucas.teixeira@email.com', telefone='(16) 99010-0010',
             tipo_contato='emergencia',
             responsavel_nome='Simone Teixeira', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99010-0010'),

        dict(matricula='2026-G003', nome='Camila Rocha Guimarães',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='2º semestre', turma='B', turno='noite',
             data_nascimento='2006-05-29', cpf='111.222.333-00',
             email='camila.guimaraes@email.com', telefone='(16) 99111-0011',
             tipo_contato='emergencia',
             responsavel_nome='Nelson Guimarães', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99111-0011', responsavel_email='nelson.g@email.com'),

        dict(matricula='2026-G004', nome='Pedro Augusto Rezende',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='3º semestre', turma='A', turno='manhã',
             data_nascimento='2005-10-07', cpf='222.333.444-11',
             email='pedro.rezende@email.com', telefone='(16) 99212-0012',
             tipo_contato='emergencia',
             responsavel_nome='Cristina Rezende', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99212-0012'),

        dict(matricula='2026-G005', nome='Natália Vasconcelos Lima',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='3º semestre', turma='B', turno='tarde',
             data_nascimento='2005-03-21', cpf='333.444.555-22',
             email='natalia.lima@email.com', telefone='(16) 99313-0013',
             tipo_contato='emergencia',
             responsavel_nome='Márcio Lima', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99313-0013', responsavel_email='marcio.lima@email.com'),

        dict(matricula='2026-G006', nome='Thiago Mendonça Pereira',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='4º semestre', turma='B', turno='noite',
             data_nascimento='2004-07-16', cpf='444.555.666-33',
             email='thiago.pereira@email.com', telefone='(16) 99414-0014',
             tipo_contato='emergencia',
             responsavel_nome='Lúcia Pereira', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99414-0014'),

        dict(matricula='2026-G007', nome='Bruna Monteiro Cardoso',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='5º semestre', turma='A', turno='manhã',
             data_nascimento='2004-11-30', cpf='555.666.777-44',
             email='bruna.cardoso@email.com', telefone='(16) 99515-0015',
             tipo_contato='emergencia',
             responsavel_nome='Rogério Cardoso', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99515-0015', responsavel_email='rogerio.c@email.com'),

        dict(matricula='2026-G008', nome='Diego Albuquerque Freitas',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='5º semestre', turma='A', turno='tarde',
             data_nascimento='2003-04-08', cpf='666.777.888-55',
             email='diego.freitas@email.com', telefone='(16) 99616-0016',
             tipo_contato='emergencia',
             responsavel_nome='Eliane Freitas', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99616-0016'),

        dict(matricula='2026-G009', nome='Júlia Esteves Marinho',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='6º semestre', turma='B', turno='noite',
             data_nascimento='2002-08-23', cpf='777.888.999-66',
             email='julia.marinho@email.com', telefone='(16) 99717-0017',
             tipo_contato='emergencia',
             responsavel_nome='Flávio Marinho', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99717-0017', responsavel_email='flavio.m@email.com'),

        dict(matricula='2026-G010', nome='Rafael Cunha Nogueira',
             nivel='graduacao', curso='Tecnologia em Mecatrônica Industrial',
             serie='7º semestre', turma='A', turno='manhã',
             data_nascimento='2001-01-14', cpf='888.999.000-77',
             email='rafael.nogueira@email.com', telefone='(16) 99818-0018',
             tipo_contato='emergencia',
             responsavel_nome='Aparecida Nogueira', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99818-0018'),

        # ── PÓS-GRADUAÇÃO ──────────────────────────────────────────────
        dict(matricula='2026-P001', nome='Mariana Costa Drummond',
             nivel='pos', curso='Pós-Graduação em Indústria Digital',
             serie='1º semestre', turma='A', turno='noite',
             data_nascimento='2001-12-05', cpf='123.456.789-00',
             email='mariana.drummond@email.com', telefone='(16) 99919-0019',
             tipo_contato='emergencia',
             responsavel_nome='Paulo Drummond', responsavel_parentesco='Pai',
             responsavel_contato='(16) 99919-0019', responsavel_email='paulo.drum@email.com'),

        dict(matricula='2026-P002', nome='Felipe Andrade Mota',
             nivel='pos', curso='Pós-Graduação em Automação da Manufatura',
             serie='1º semestre', turma='B', turno='noite',
             data_nascimento='2000-05-18', cpf='987.654.321-00',
             email='felipe.mota@email.com', telefone='(16) 99020-0020',
             tipo_contato='emergencia',
             responsavel_nome='Sandra Mota', responsavel_parentesco='Mãe',
             responsavel_contato='(16) 99020-0020'),
    ]

    alunos = []
    print("\n── ALUNOS ───────────────────────────────")
    for a in alunos_data:
        ex = Aluno.query.filter_by(matricula=a['matricula']).first()
        if not ex:
            dn = datetime.strptime(a.pop('data_nascimento'), '%Y-%m-%d').date()
            novo = Aluno(data_nascimento=dn, **a)
            db.session.add(novo)
            alunos.append(novo)
            nivel_label = {'tecnico': 'Téc', 'graduacao': 'Grad', 'pos': 'Pós'}.get(novo.nivel, novo.nivel)
            print(f"  ✓ {novo.nome:<32} {nivel_label} · {novo.serie} · {novo.turno}")
        else:
            alunos.append(ex)
            print(f"  — Já existe: {a['nome']}")
    db.session.commit()

    # ─────────────────────────────────────────
    # OCORRÊNCIAS
    # ─────────────────────────────────────────
    def log(oc_id, acao, desc, usuario, dias, sigiloso=False):
        db.session.add(LogAuditoria(
            ocorrencia_id=oc_id, usuario_id=usuario.id,
            acao=acao, descricao_acao=desc, sigiloso=sigiloso,
            data_hora=agora(dias)
        ))

    def criar(aluno, tipo, status, criado_por, responsavel, descricao, dias_criacao, logs_data, dias_enc=None):
        o = Ocorrencia(
            aluno_id=aluno.id, tipo=tipo, status=status,
            criado_por_id=criado_por.id, responsavel_id=responsavel.id,
            descricao=descricao, data_criacao=agora(dias_criacao),
            data_encerramento=agora(dias_enc) if dias_enc else None
        )
        db.session.add(o)
        db.session.flush()
        for acao, usuario, desc, dias, *extra in logs_data:
            sigiloso = extra[0] if extra else False
            log(o.id, acao, desc, usuario, dias, sigiloso)
        return o

    print("\n── OCORRÊNCIAS ──────────────────────────")
    ocorrencias = [

        # ── ENCERRADAS ────────────────────────────────────────────────
        criar(alunos[1], 'Disciplinar', 'encerrada', ana, marcos,
              'Aluno envolveu-se em discussão com colega durante aula prática de laboratório. '
              'Comportamento agressivo relatado pelo professor responsável.',
              22, [
                  ('criada',     ana,    'Ocorrência criada por Ana Lima.', 22),
                  ('encaminhada',ana,    'Encaminhada de Ana Lima para Marcos Ribeiro (coordenacao).\nMotivo: Situação requer análise da coordenação.', 21),
                  ('atualizada', marcos, 'Andamento registrado por Marcos Ribeiro: Conversa realizada com o aluno. Responsável convocado para reunião.', 18),
                  ('encerrada',  marcos, 'Encerrada por Marcos Ribeiro.\nResolução: Reunião realizada. Acordo de comportamento firmado. Aluno ciente das normas do curso.', 15),
              ], 15),

        criar(alunos[4], 'Saúde', 'encerrada', carlos, juliana,
              'Aluna relatou crise de ansiedade durante prova prática. '
              'Insônia e dificuldade de concentração nas últimas semanas.',
              18, [
                  ('criada',     carlos,  'Ocorrência criada por Carlos Menezes.', 18),
                  ('encaminhada',carlos,  'Encaminhada de Carlos Menezes para Juliana Cardoso (coordenacao).\nMotivo: Saúde mental requer acompanhamento especializado.', 17),
                  ('encerrada',  juliana, 'Encerrada por Juliana Cardoso.\nResolução: Aluna encaminhada para psicólogo parceiro. Professores notificados sobre adaptações necessárias.', 14),
              ], 14),

        criar(alunos[11], 'Financeiro', 'encerrada', patricia, marcos,
              'Aluno com mensalidades em atraso há 2 meses. '
              'Relatou dificuldades financeiras após desemprego do responsável financeiro.',
              30, [
                  ('criada',     patricia, 'Ocorrência criada por Patrícia Souza.', 30),
                  ('encaminhada',patricia, 'Encaminhada de Patrícia Souza para Marcos Ribeiro (coordenacao).\nMotivo: Necessita análise para programa de bolsa/auxílio.', 29),
                  ('atualizada', marcos,   'Andamento registrado por Marcos Ribeiro: Família encaminhada ao setor financeiro. Documentação para bolsa social solicitada.', 25),
                  ('encerrada',  marcos,   'Encerrada por Marcos Ribeiro.\nResolução: Aluno incluído no programa de bolsa social. Parcelas renegociadas. Situação regularizada.', 22),
              ], 22),

        criar(alunos[8], 'Evasão', 'encerrada', fernanda, juliana,
              'Aluna com 6 faltas consecutivas sem justificativa no 1º semestre. '
              'Contato com a família ainda não havia sido realizado.',
              25, [
                  ('criada',     fernanda, 'Ocorrência criada por Fernanda Prado.', 25),
                  ('encaminhada',fernanda, 'Encaminhada de Fernanda Prado para Juliana Cardoso (coordenacao).\nMotivo: Risco de evasão — intervenção urgente necessária.', 24),
                  ('atualizada', juliana,  'Andamento registrado por Juliana Cardoso: Contato realizado com a aluna. Relatou dificuldades de adaptação ao ritmo do curso.', 20),
                  ('atualizada', juliana,  'Andamento registrado por Juliana Cardoso: Plano de acompanhamento montado junto à pedagoga. Aluna retornou às aulas regularmente.', 17, True),
                  ('encerrada',  juliana,  'Encerrada por Juliana Cardoso.\nResolução: Frequência normalizada. Acompanhamento quinzenal mantido com a pedagoga.', 15),
              ], 15),

        # ── EM ANDAMENTO ──────────────────────────────────────────────
        criar(alunos[6], 'Psicossocial', 'em_andamento', ana, marcos,
              'Aluna demonstra sinais de sofrimento emocional — isolamento, choro frequente '
              'em sala e relatos de conflitos familiares sérios.',
              10, [
                  ('criada',     ana,    'Ocorrência criada por Ana Lima.', 10),
                  ('encaminhada',ana,    'Encaminhada de Ana Lima para Marcos Ribeiro (coordenacao).\nMotivo: Situação emocional requer acompanhamento especializado.', 9),
                  ('atualizada', marcos, 'Andamento registrado por Marcos Ribeiro: Conversa acolhedora realizada. Encaminhamento para psicólogo parceiro. Primeira consulta agendada.', 6),
                  ('atualizada', marcos, 'Andamento registrado por Marcos Ribeiro: Aluna compareceu à primeira consulta. Evolução positiva relatada. Próxima sessão em 15 dias.', 3, True),
              ]),

        criar(alunos[12], 'Acadêmico', 'em_andamento', carlos, fernanda,
              'Aluno com queda brusca de rendimento no 3º semestre. Média geral caiu de 7,8 '
              'para 4,2. Professores relatam dificuldades com cálculo diferencial.',
              7, [
                  ('criada',     carlos,   'Ocorrência criada por Carlos Menezes.', 7),
                  ('encaminhada',carlos,   'Encaminhada de Carlos Menezes para Fernanda Prado (pedagogia).\nMotivo: Queda de rendimento requer acompanhamento pedagógico.', 6),
                  ('atualizada', fernanda, 'Andamento registrado por Fernanda Prado: Conversa realizada. Dificuldades em Cálculo II identificadas. Monitor de reforço indicado.', 4),
                  ('atualizada', fernanda, 'Andamento registrado por Fernanda Prado: Aluno iniciou reforço com monitor. Professores de Cálculo notificados.', 2),
              ]),

        criar(alunos[9], 'Evasão', 'em_andamento', patricia, rodrigo,
              'Aluno do 1º semestre com 4 faltas na última semana. Relatou dificuldades de '
              'adaptação ao ensino superior e pensamentos de desistência do curso.',
              8, [
                  ('criada',     patricia, 'Ocorrência criada por Patrícia Souza.', 8),
                  ('encaminhada',patricia, 'Encaminhada de Patrícia Souza para Rodrigo Bastos (pedagogia).\nMotivo: Risco de evasão no 1º semestre — intervenção pedagógica necessária.', 7),
                  ('atualizada', rodrigo,  'Andamento registrado por Rodrigo Bastos: Sessão de acolhimento realizada. Aluno relatou dificuldades com o volume de conteúdo. Plano de apoio montado.', 5),
              ]),

        criar(alunos[18], 'Psicossocial', 'em_andamento', ana, marcos,
              'Aluna relata síndrome de burnout — exaustão intensa, dificuldade de '
              'concentração e choro frequente. Próxima ao TCC com alta pressão.',
              5, [
                  ('criada',     ana,    'Ocorrência criada por Ana Lima.', 5),
                  ('encaminhada',ana,    'Encaminhada de Ana Lima para Marcos Ribeiro (coordenacao).\nMotivo: Burnout em fase crítica do curso requer atenção imediata.', 4),
                  ('atualizada', marcos, 'Andamento registrado por Marcos Ribeiro: Conversa realizada. Orientador do TCC notificado. Prazo negociado com a coordenação.', 2, True),
              ]),

        # ── ABERTAS ───────────────────────────────────────────────────
        criar(alunos[0], 'Acadêmico', 'aberta', ana, ana,
              'Aluna do 1º semestre de Técnico em Mecatrônica com dificuldades em '
              'eletricidade básica. Professora relatou baixo rendimento nas atividades práticas.',
              2, [('criada', ana, 'Ocorrência criada por Ana Lima.', 2)]),

        criar(alunos[13], 'Disciplinar', 'aberta', carlos, carlos,
              'Aluno flagrado utilizando celular durante avaliação, configurando possível cola. '
              'Professor encaminhou ao setor de apoio para registro formal conforme regimento.',
              1, [('criada', carlos, 'Ocorrência criada por Carlos Menezes.', 1)]),

        criar(alunos[2], 'Financeiro', 'aberta', patricia, patricia,
              'Aluna solicitou informações sobre bolsas e programas de auxílio financeiro. '
              'Relatou dificuldade em manter mensalidades após redução de renda familiar.',
              1, [('criada', patricia, 'Ocorrência criada por Patrícia Souza.', 1)]),

        criar(alunos[16], 'Evasão', 'aberta', ana, ana,
              'Aluno do 6º semestre com frequência abaixo de 75% em 3 disciplinas. '
              'Não respondeu aos contatos anteriores. Risco real de reprovação por falta.',
              0, [('criada', ana, 'Ocorrência criada por Ana Lima.', 0)]),

        criar(alunos[19], 'Psicossocial', 'aberta', carlos, carlos,
              'Aluno relata pressão excessiva e possível assédio moral por parte do supervisor '
              'durante estágio obrigatório. Situação requer apuração urgente.',
              0, [('criada', carlos, 'Ocorrência criada por Carlos Menezes.', 0)]),

        # Gabriel — reincidente (2ª ocorrência)
        criar(alunos[1], 'Disciplinar', 'aberta', patricia, patricia,
              'Segunda ocorrência disciplinar do aluno no semestre. Recusa em participar de '
              'atividade em grupo e desrespeito verbal ao colega de turma.',
              3, [('criada', patricia, 'Ocorrência criada por Patrícia Souza.', 3)]),
    ]

    db.session.commit()

    enc  = sum(1 for o in ocorrencias if o.status == 'encerrada')
    and_ = sum(1 for o in ocorrencias if o.status == 'em_andamento')
    ab   = sum(1 for o in ocorrencias if o.status == 'aberta')

    print(f"\n── RESUMO ───────────────────────────────")
    print(f"  Usuários    : 8")
    print(f"  Alunos      : {len(alunos_data)} (8 técnico · 10 graduação · 2 pós)")
    print(f"  Ocorrências : {len(ocorrencias)} ({enc} encerradas · {and_} em andamento · {ab} abertas)")
    print(f"\n{'='*52}")
    print(f"✓ Seed concluído com sucesso!")
    print(f"{'='*52}")
    print(f"\nCredenciais de acesso (@sirae.com.br):")
    print(f"  admin@sirae.com.br      / admin123  → Administrador")
    print(f"  ana.lima@sirae.com.br   / 123456    → Atendente")
    print(f"  carlos.m@sirae.com.br   / 123456    → Atendente")
    print(f"  patricia@sirae.com.br   / 123456    → Atendente")
    print(f"  fernanda.p@sirae.com.br / 123456    → Pedagogo")
    print(f"  rodrigo.b@sirae.com.br  / 123456    → Pedagogo")
    print(f"  marcos.r@sirae.com.br   / 123456    → Coordenação")
    print(f"  juliana.c@sirae.com.br  / 123456    → Coordenação")
    print(f"\n  Acesse: http://localhost:5000")
