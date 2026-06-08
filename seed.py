"""
Seed completo do SIRAE — usuários, alunos e ocorrências de exemplo.
Execute: python seed.py
"""
from app import create_app, db
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from app.models.ocorrencia import Ocorrencia, LogAuditoria
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    db.create_all()

    # ─────────────────────────────────────────
    # USUÁRIOS
    # ─────────────────────────────────────────
    usuarios_data = [
        {'email': 'admin@sirae.com',     'nome': 'Administrador',       'perfil': 'admin',       'senha': 'admin123'},
        {'email': 'ana.lima@sirae.com',  'nome': 'Ana Lima',            'perfil': 'atendente',   'senha': '123456'},
        {'email': 'carlos.m@sirae.com',  'nome': 'Carlos Menezes',      'perfil': 'atendente',   'senha': '123456'},
        {'email': 'patricia@sirae.com',  'nome': 'Patrícia Souza',      'perfil': 'atendente',   'senha': '123456'},
        {'email': 'marcos.r@sirae.com',  'nome': 'Marcos Ribeiro',      'perfil': 'coordenacao', 'senha': '123456'},
        {'email': 'juliana.c@sirae.com', 'nome': 'Juliana Cardoso',     'perfil': 'coordenacao', 'senha': '123456'},
    ]

    usuarios = {}
    print("\n── USUÁRIOS ─────────────────────────────")
    for u in usuarios_data:
        existente = Usuario.query.filter_by(email=u['email']).first()
        if not existente:
            novo = Usuario(email=u['email'], nome=u['nome'], perfil=u['perfil'])
            novo.set_password(u['senha'])
            db.session.add(novo)
            db.session.flush()
            usuarios[u['email']] = novo
            print(f"  ✅ {u['nome']:<25} [{u['perfil']:<12}] — {u['email']} / {u['senha']}")
        else:
            usuarios[u['email']] = existente
            print(f"  ℹ️  Já existe: {u['email']}")

    db.session.commit()

    # Atalhos
    ana      = usuarios['ana.lima@sirae.com']
    carlos   = usuarios['carlos.m@sirae.com']
    patricia = usuarios['patricia@sirae.com']
    marcos   = usuarios['marcos.r@sirae.com']
    juliana  = usuarios['juliana.c@sirae.com']

    # ─────────────────────────────────────────
    # ALUNOS
    # ─────────────────────────────────────────
    alunos_data = [
        # Fundamental
        dict(nome='Beatriz Moraes Alves',     matricula='2026-0001', nivel='fundamental', serie='6º ano EF', turma='A', turno='manhã',
             data_nascimento='2013-03-15', cpf='111.222.333-44',
             responsavel_nome='Sônia Alves', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99101-1111', responsavel_email='sonia.alves@email.com'),

        dict(nome='Gabriel Henrique Campos',  matricula='2026-0002', nivel='fundamental', serie='6º ano EF', turma='A', turno='manhã',
             data_nascimento='2013-07-22', cpf='222.333.444-55',
             responsavel_nome='Roberto Campos', responsavel_parentesco='Pai',
             responsavel_contato='(44) 99202-2222'),

        dict(nome='Larissa Pinto Cavalcanti',  matricula='2026-0003', nivel='fundamental', serie='7º ano EF', turma='B', turno='tarde',
             data_nascimento='2012-11-08', cpf='333.444.555-66',
             responsavel_nome='Fátima Cavalcanti', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99303-3333', responsavel_email='fatima.cav@email.com'),

        dict(nome='Mateus Oliveira Brandão',   matricula='2026-0004', nivel='fundamental', serie='7º ano EF', turma='B', turno='tarde',
             data_nascimento='2012-04-30', cpf='444.555.666-77',
             responsavel_nome='Denise Brandão', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99404-4444'),

        dict(nome='Fernanda Castro Duarte',    matricula='2026-0005', nivel='fundamental', serie='8º ano EF', turma='C', turno='manhã',
             data_nascimento='2011-09-14', cpf='555.666.777-88',
             responsavel_nome='Cláudio Duarte', responsavel_parentesco='Pai',
             responsavel_contato='(44) 99505-5555', responsavel_email='claudio.duarte@email.com'),

        dict(nome='Vinícius Torres Magalhães', matricula='2026-0006', nivel='fundamental', serie='8º ano EF', turma='C', turno='manhã',
             data_nascimento='2011-01-19', cpf='666.777.888-99',
             responsavel_nome='Rosana Magalhães', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99606-6666'),

        dict(nome='Isabela Nunes Figueiredo',  matricula='2026-0007', nivel='fundamental', serie='9º ano EF', turma='A', turno='tarde',
             data_nascimento='2010-06-25', cpf='777.888.999-00',
             responsavel_nome='Eduardo Figueiredo', responsavel_parentesco='Pai',
             responsavel_contato='(44) 99707-7777', responsavel_email='edu.figueiredo@email.com'),

        dict(nome='Rodrigo Sampaio Correia',   matricula='2026-0008', nivel='fundamental', serie='9º ano EF', turma='A', turno='tarde',
             data_nascimento='2010-12-03', cpf='888.999.000-11',
             responsavel_nome='Vera Correia', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99808-8888'),

        # Médio
        dict(nome='Amanda Ferreira Queiroz',   matricula='2026-0009', nivel='medio', serie='1º ano EM', turma='A', turno='manhã',
             data_nascimento='2009-02-17', cpf='999.000.111-22',
             responsavel_nome='Antônio Queiroz', responsavel_parentesco='Pai',
             responsavel_contato='(44) 99909-9999', responsavel_email='antonio.q@email.com'),

        dict(nome='Lucas Barbosa Teixeira',    matricula='2026-0010', nivel='medio', serie='1º ano EM', turma='A', turno='manhã',
             data_nascimento='2009-08-11', cpf='000.111.222-33',
             responsavel_nome='Simone Teixeira', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99010-0000'),

        dict(nome='Camila Rocha Guimarães',    matricula='2026-0011', nivel='medio', serie='1º ano EM', turma='B', turno='noite',
             data_nascimento='2009-05-29', cpf='111.222.333-00',
             responsavel_nome='Nelson Guimarães', responsavel_parentesco='Pai',
             responsavel_contato='(44) 99111-1100', responsavel_email='nelson.g@email.com'),

        dict(nome='Pedro Augusto Rezende',     matricula='2026-0012', nivel='medio', serie='2º ano EM', turma='A', turno='manhã',
             data_nascimento='2008-10-07', cpf='222.333.444-11',
             responsavel_nome='Cristina Rezende', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99212-1200'),

        dict(nome='Natália Vasconcelos Lima',  matricula='2026-0013', nivel='medio', serie='2º ano EM', turma='B', turno='tarde',
             data_nascimento='2008-03-21', cpf='333.444.555-22',
             responsavel_nome='Márcio Lima', responsavel_parentesco='Pai',
             responsavel_contato='(44) 99313-1300', responsavel_email='marcio.lima@email.com'),

        dict(nome='Thiago Mendonça Pereira',   matricula='2026-0014', nivel='medio', serie='2º ano EM', turma='B', turno='tarde',
             data_nascimento='2008-07-16', cpf='444.555.666-33',
             responsavel_nome='Lúcia Pereira', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99414-1400'),

        dict(nome='Bruna Monteiro Cardoso',    matricula='2026-0015', nivel='medio', serie='3º ano EM', turma='A', turno='manhã',
             data_nascimento='2007-11-30', cpf='555.666.777-44',
             responsavel_nome='Rogério Cardoso', responsavel_parentesco='Pai',
             responsavel_contato='(44) 99515-1500', responsavel_email='rogerio.c@email.com'),

        dict(nome='Diego Albuquerque Freitas', matricula='2026-0016', nivel='medio', serie='3º ano EM', turma='A', turno='manhã',
             data_nascimento='2007-04-08', cpf='666.777.888-55',
             responsavel_nome='Eliane Freitas', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99616-1600'),

        dict(nome='Júlia Esteves Marinho',     matricula='2026-0017', nivel='medio', serie='3º ano EM', turma='B', turno='noite',
             data_nascimento='2007-08-23', cpf='777.888.999-66',
             responsavel_nome='Flávio Marinho', responsavel_parentesco='Pai',
             responsavel_contato='(44) 99717-1700', responsavel_email='flavio.m@email.com'),

        dict(nome='Rafael Cunha Nogueira',     matricula='2026-0018', nivel='medio', serie='3º ano EM', turma='B', turno='noite',
             data_nascimento='2007-01-14', cpf='888.999.000-77',
             responsavel_nome='Aparecida Nogueira', responsavel_parentesco='Mãe',
             responsavel_contato='(44) 99818-1800'),
    ]

    alunos = []
    print("\n── ALUNOS ───────────────────────────────")
    for a in alunos_data:
        existente = Aluno.query.filter_by(matricula=a['matricula']).first()
        if not existente:
            dn = datetime.strptime(a.pop('data_nascimento'), '%Y-%m-%d').date()
            novo = Aluno(data_nascimento=dn, **a)
            db.session.add(novo)
            alunos.append(novo)
            print(f"  ✅ {novo.nome:<30} {novo.serie} / Turma {novo.turma} / {novo.turno}")
        else:
            alunos.append(existente)
            print(f"  ℹ️  Já existe: {a['nome']}")

    db.session.commit()

    # ─────────────────────────────────────────
    # OCORRÊNCIAS
    # ─────────────────────────────────────────
    def dp(dias):
        return datetime.utcnow() - timedelta(days=dias)

    ocorrencias_data = [
        # Encerradas
        dict(aluno=alunos[1], tipo='Disciplinar', status='encerrada',
             criado_por=ana, responsavel=marcos, data_criacao=dp(20), data_encerramento=dp(15),
             descricao='Aluno apresentou comportamento inadequado em sala, com discussão com colega durante aula de Matemática. Professora relatou o ocorrido.',
             logs=[
                 ('criada',     ana,    'Ocorrência criada por Ana Lima para o aluno Gabriel Henrique Campos', 20),
                 ('encaminhada',ana,    'Encaminhada de Ana Lima para Marcos Ribeiro (coordenacao). Motivo: Requer análise da coordenação.', 19),
                 ('encerrada',  marcos, 'Encerrada por Marcos Ribeiro. Resolução: Conversa com aluno e responsável. Acordo de comportamento firmado.', 15),
             ]),

        dict(aluno=alunos[4], tipo='Saúde', status='encerrada',
             criado_por=carlos, responsavel=juliana, data_criacao=dp(18), data_encerramento=dp(10),
             descricao='Aluna relatou mal-estar durante aula, com tonturas e dores de cabeça. Responsável foi acionado e veio buscá-la.',
             logs=[
                 ('criada',     carlos,  'Ocorrência criada por Carlos Menezes para a aluna Fernanda Castro Duarte', 18),
                 ('encaminhada',carlos,  'Encaminhada de Carlos Menezes para Juliana Cardoso (coordenacao). Motivo: Saúde requer acompanhamento.', 17),
                 ('encerrada',  juliana, 'Encerrada por Juliana Cardoso. Resolução: Responsável acionado. Aluna encaminhada ao médico. Atestado entregue.', 10),
             ]),

        dict(aluno=alunos[11], tipo='Financeiro', status='encerrada',
             criado_por=patricia, responsavel=marcos, data_criacao=dp(25), data_encerramento=dp(20),
             descricao='Família com pendências financeiras há 2 meses. Aluno em situação de vulnerabilidade socioeconômica.',
             logs=[
                 ('criada',     patricia, 'Ocorrência criada por Patrícia Souza para o aluno Pedro Augusto Rezende', 25),
                 ('encaminhada',patricia, 'Encaminhada de Patrícia Souza para Marcos Ribeiro (coordenacao). Motivo: Análise para possível bolsa social.', 24),
                 ('encerrada',  marcos,   'Encerrada por Marcos Ribeiro. Resolução: Família encaminhada ao financeiro. Acordo de parcelamento firmado.', 20),
             ]),

        # Em acompanhamento
        dict(aluno=alunos[6], tipo='Familiar', status='em_acompanhamento',
             criado_por=ana, responsavel=marcos, data_criacao=dp(8),
             descricao='Aluna tem faltado com frequência. Contato com responsável revelou situação familiar delicada — pais em separação litigiosa.',
             logs=[
                 ('criada',     ana,    'Ocorrência criada por Ana Lima para a aluna Isabela Nunes Figueiredo', 8),
                 ('encaminhada',ana,    'Encaminhada de Ana Lima para Marcos Ribeiro (coordenacao). Motivo: Situação familiar complexa.', 7),
                 ('atualizada', marcos, 'Contato com assistente social agendado para a próxima semana.', 5),
             ]),

        dict(aluno=alunos[12], tipo='Acadêmico', status='em_acompanhamento',
             criado_por=carlos, responsavel=carlos, data_criacao=dp(5),
             descricao='Aluna com queda brusca de notas no 2º bimestre. Média caiu de 8,2 para 4,1. Professores relatam desatenção e falta de participação.',
             logs=[
                 ('criada',     carlos, 'Ocorrência criada por Carlos Menezes para a aluna Natália Vasconcelos Lima', 5),
                 ('atualizada', carlos, 'Agenda de reforço escolar montada. Encaminhado para Pedagogia.', 3),
             ]),

        dict(aluno=alunos[9], tipo='Disciplinar', status='em_acompanhamento',
             criado_por=patricia, responsavel=juliana, data_criacao=dp(6),
             descricao='Aluno envolvido em episódio de bullying com colega de turma. Situação confirmada por professora e outros alunos.',
             logs=[
                 ('criada',     patricia, 'Ocorrência criada por Patrícia Souza para o aluno Lucas Barbosa Teixeira', 6),
                 ('encaminhada',patricia, 'Encaminhada de Patrícia Souza para Juliana Cardoso (coordenacao). Motivo: Bullying requer intervenção imediata.', 5),
                 ('atualizada', juliana,  'Conversa realizada com as partes. Responsáveis convocados para reunião.', 4),
             ]),

        # Abertas
        dict(aluno=alunos[0], tipo='Saúde', status='aberta',
             criado_por=ana, responsavel=ana, data_criacao=dp(2),
             descricao='Aluna relatou sintomas de ansiedade intensa antes das provas. Choro frequente e relatos de insônia. Indicado acompanhamento psicológico.',
             logs=[('criada', ana, 'Ocorrência criada por Ana Lima para a aluna Beatriz Moraes Alves', 2)]),

        dict(aluno=alunos[13], tipo='Disciplinar', status='aberta',
             criado_por=carlos, responsavel=carlos, data_criacao=dp(1),
             descricao='Aluno flagrado com celular durante prova, configurando possível cola. Professor encaminhou ao setor de apoio para registro formal.',
             logs=[('criada', carlos, 'Ocorrência criada por Carlos Menezes para o aluno Thiago Mendonça Pereira', 1)]),

        dict(aluno=alunos[2], tipo='Financeiro', status='aberta',
             criado_por=patricia, responsavel=patricia, data_criacao=dp(1),
             descricao='Família solicitou informações sobre isenção de taxa de material didático. Situação de vulnerabilidade socioeconômica relatada.',
             logs=[('criada', patricia, 'Ocorrência criada por Patrícia Souza para a aluna Larissa Pinto Cavalcanti', 1)]),

        dict(aluno=alunos[16], tipo='Acadêmico', status='aberta',
             criado_por=ana, responsavel=ana, data_criacao=dp(0),
             descricao='Aluna do 3º ano EM com frequência abaixo de 75% no mês. Risco de reprovação por falta. Responsável ainda não foi contatado.',
             logs=[('criada', ana, 'Ocorrência criada por Ana Lima para a aluna Júlia Esteves Marinho', 0)]),

        # Reincidente (Gabriel — 2ª ocorrência)
        dict(aluno=alunos[1], tipo='Disciplinar', status='aberta',
             criado_por=carlos, responsavel=carlos, data_criacao=dp(3),
             descricao='Segunda ocorrência disciplinar do mês. Aluno desrespeitou verbalmente o professor durante aula de Educação Física.',
             logs=[('criada', carlos, 'Ocorrência criada por Carlos Menezes para o aluno Gabriel Henrique Campos', 3)]),
    ]

    print("\n── OCORRÊNCIAS ──────────────────────────")
    for o_data in ocorrencias_data:
        logs_data       = o_data.pop('logs')
        data_enc        = o_data.pop('data_encerramento', None)
        data_cria       = o_data.pop('data_criacao')
        aluno           = o_data.pop('aluno')
        criado_por      = o_data.pop('criado_por')
        responsavel     = o_data.pop('responsavel')

        o = Ocorrencia(
            aluno_id=aluno.id,
            criado_por_id=criado_por.id,
            responsavel_id=responsavel.id,
            data_criacao=data_cria,
            data_encerramento=data_enc,
            **o_data
        )
        db.session.add(o)
        db.session.flush()

        for acao, usuario, descricao, dias_atras in logs_data:
            db.session.add(LogAuditoria(
                ocorrencia_id=o.id,
                usuario_id=usuario.id,
                acao=acao,
                descricao_acao=descricao,
                data_hora=datetime.utcnow() - timedelta(days=dias_atras)
            ))

        print(f"  ✅ #{o.id:04d} {aluno.nome:<30} [{o.status:<18}] {o.tipo}")

    db.session.commit()

    print("\n" + "="*55)
    print("✅ Seed concluído!")
    print("="*55)
    print(f"\n  Usuários    : {len(usuarios_data)}")
    print(f"  Alunos      : {len(alunos_data)}")
    print(f"  Ocorrências : {len(ocorrencias_data)}")
    print("\nCredenciais:")
    print("  admin@sirae.com      / admin123  → Administrador")
    print("  ana.lima@sirae.com   / 123456    → Atendente")
    print("  carlos.m@sirae.com   / 123456    → Atendente")
    print("  patricia@sirae.com   / 123456    → Atendente")
    print("  marcos.r@sirae.com   / 123456    → Coordenação")
    print("  juliana.c@sirae.com  / 123456    → Coordenação")
    print("\nAcesse: http://localhost:5000")
