import re
import os
import time
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from app.models.aluno import Aluno, formatar_cpf, formatar_telefone, limpar_numeros
from app.models.log_aluno import LogAluno
from app import db
from datetime import datetime, date

aluno_bp = Blueprint('alunos', __name__, url_prefix='/alunos')

FOTO_EXTS = {'jpg', 'jpeg', 'png', 'webp'}


def salvar_foto(arquivo, aluno_id):
    """Salva foto do aluno e retorna o nome do arquivo"""
    ext = arquivo.filename.rsplit('.', 1)[-1].lower()
    if ext not in FOTO_EXTS:
        return None, 'Formato de foto inválido. Use JPG, PNG ou WEBP.'
    pasta = os.path.join(current_app.root_path, 'static', 'uploads', 'fotos')
    os.makedirs(pasta, exist_ok=True)
    nome = f'aluno_{aluno_id}_{int(time.time())}.{ext}'
    arquivo.save(os.path.join(pasta, nome))
    return f'uploads/fotos/{nome}', None


def extrair_form(form):
    """Extrai e valida os campos do formulário. Retorna (dados, erros)"""
    erros = []

    nome = form.get('nome', '').strip()
    if not nome:
        erros.append('O nome é obrigatório.')
    elif not re.match(r"^[a-zA-ZÀ-ÿ\s'\-]+$", nome):
        erros.append('Nome deve conter apenas letras e espaços.')

    # CPF — valida apenas se preenchido
    cpf_raw = form.get('cpf', '').strip()
    cpf = None
    if cpf_raw:
        nums = limpar_numeros(cpf_raw)
        if len(nums) != 11:
            erros.append('CPF deve ter 11 dígitos.')
        else:
            cpf = formatar_cpf(cpf_raw)

    # Telefone aluno — 10 ou 11 dígitos
    tel_raw = form.get('telefone', '').strip()
    telefone = None
    if tel_raw:
        nums_tel = limpar_numeros(tel_raw)
        if len(nums_tel) not in (10, 11):
            erros.append('Telefone do aluno deve ter 10 ou 11 dígitos (com DDD).')
        else:
            telefone = formatar_telefone(tel_raw)

    # Telefone responsável
    resp_tel_raw = form.get('responsavel_contato', '').strip()
    responsavel_contato = None
    if resp_tel_raw:
        nums_rt = limpar_numeros(resp_tel_raw)
        if len(nums_rt) not in (10, 11):
            erros.append('Telefone do responsável deve ter 10 ou 11 dígitos (com DDD).')
        else:
            responsavel_contato = formatar_telefone(resp_tel_raw)

    # CPF responsável
    resp_cpf_raw = form.get('responsavel_cpf', '').strip()
    responsavel_cpf = None
    if resp_cpf_raw:
        if len(limpar_numeros(resp_cpf_raw)) != 11:
            erros.append('CPF do responsável deve ter 11 dígitos.')
        else:
            responsavel_cpf = formatar_cpf(resp_cpf_raw)

    # Matrícula — máx 20 chars alfanuméricos
    matricula = (form.get('matricula', '').strip().upper()) or None
    if not matricula:
        erros.append('A matrícula é obrigatória.')
    elif len(matricula) > 20:
        erros.append('Matrícula deve ter no máximo 20 caracteres.')

    nivel = form.get('nivel', '').strip() or None
    if not nivel:
        erros.append('O nível de ensino é obrigatório.')
    elif nivel not in ('aprendizagem', 'tecnico', 'graduacao', 'pos', 'livre'):
        erros.append('Nível de ensino inválido.')

    curso = form.get('curso', '').strip() or None
    if not curso:
        erros.append('O curso é obrigatório.')

    # Data de nascimento — obrigatória
    dn_str = form.get('data_nascimento', '').strip()
    data_nascimento = None
    if not dn_str:
        erros.append('A data de nascimento é obrigatória.')
    else:
        try:
            data_nascimento = datetime.strptime(dn_str, '%Y-%m-%d').date()
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - (
                (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
            )
            if idade > 100:
                erros.append('Data de nascimento inválida — verifique o ano informado.')
            elif idade < 14:
                erros.append('A idade mínima para cadastro é 14 anos.')
            elif idade < 18:
                # Menor — responsável legal obrigatório completo
                if not form.get('responsavel_nome', '').strip():
                    erros.append('Nome do responsável é obrigatório para alunos menores de 18 anos.')
                if not form.get('responsavel_contato', '').strip():
                    erros.append('Telefone do responsável é obrigatório para alunos menores de 18 anos.')
                if not form.get('responsavel_cpf', '').strip():
                    erros.append('CPF do responsável é obrigatório para alunos menores de 18 anos.')
                if not form.get('responsavel_parentesco', '').strip():
                    erros.append('Parentesco é obrigatório para alunos menores de 18 anos.')
            else:
                # Maior — CPF, telefone + contato de emergência obrigatórios
                cpf_raw = limpar_numeros(form.get('cpf', ''))
                if not cpf_raw:
                    erros.append('CPF é obrigatório para alunos maiores de 18 anos.')
                if not tel_raw:
                    erros.append('Telefone/WhatsApp é obrigatório para alunos maiores de 18 anos.')
                if not form.get('responsavel_nome', '').strip():
                    erros.append('Nome do contato de emergência é obrigatório.')
                if not form.get('responsavel_contato', '').strip():
                    erros.append('Telefone do contato de emergência é obrigatório.')
        except ValueError:
            erros.append('Data de nascimento inválida.')

    dados = dict(
        nome=nome,
        cpf=cpf,
        telefone=telefone,
        email=form.get('email', '').strip() or None,
        data_nascimento=data_nascimento,
        matricula=matricula,
        nivel=nivel,
        serie=form.get('serie', '').strip() or None,
        turma=form.get('turma', '').strip() or None,
        turno=form.get('turno', '').strip() or None,
        responsavel_nome=form.get('responsavel_nome', '').strip() or None,
        tipo_contato=form.get('tipo_contato', 'emergencia').strip() or 'emergencia',
        responsavel_parentesco=form.get('responsavel_parentesco', '').strip() or None,
        responsavel_cpf=responsavel_cpf,
        responsavel_contato=responsavel_contato,
        responsavel_email=form.get('responsavel_email', '').strip() or None,
    )
    return dados, erros


@aluno_bp.route('/')
@login_required
def listar():
    filtro_nome  = request.args.get('nome', '').strip()
    filtro_nivel = request.args.get('nivel', '').strip()
    filtro_turno = request.args.get('turno', '').strip()

    query = Aluno.query
    if filtro_nome:
        query = query.filter(Aluno.nome.ilike(f'%{filtro_nome}%'))
    if filtro_nivel:
        query = query.filter(Aluno.nivel == filtro_nivel)
    if filtro_turno:
        query = query.filter(Aluno.turno == filtro_turno)

    alunos = query.order_by(Aluno.nome).all()
    return render_template('alunos/listar.html', alunos=alunos,
                           filtro_nome=filtro_nome,
                           filtro_nivel=filtro_nivel,
                           filtro_turno=filtro_turno)


@aluno_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if request.method == 'POST':
        dados, erros = extrair_form(request.form)

        # Duplicatas
        if dados['cpf'] and Aluno.query.filter_by(cpf=dados['cpf']).first():
            erros.append('Já existe um aluno cadastrado com este CPF.')
        if dados['matricula'] and Aluno.query.filter_by(matricula=dados['matricula']).first():
            erros.append('Já existe um aluno cadastrado com esta matrícula.')

        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('alunos/form.html', aluno=None, form=request.form)

        aluno = Aluno(**dados)
        db.session.add(aluno)
        db.session.flush()  # gera o id para nomear a foto

        # Foto
        foto = request.files.get('foto')
        if foto and foto.filename:
            caminho, erro_foto = salvar_foto(foto, aluno.id)
            if erro_foto:
                flash(erro_foto, 'warning')
            else:
                aluno.foto = caminho

        db.session.commit()
        flash(f'Aluno {aluno.nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('alunos.perfil', id=aluno.id))

    return render_template('alunos/form.html', aluno=None, form={})


@aluno_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    aluno = Aluno.query.get_or_404(id)

    if request.method == 'POST':
        dados, erros = extrair_form(request.form)

        # Duplicatas (excluindo o próprio aluno)
        if dados['cpf']:
            dup = Aluno.query.filter(Aluno.cpf == dados['cpf'], Aluno.id != id).first()
            if dup:
                erros.append('Já existe outro aluno com este CPF.')
        if dados['matricula']:
            dup = Aluno.query.filter(Aluno.matricula == dados['matricula'], Aluno.id != id).first()
            if dup:
                erros.append('Já existe outro aluno com esta matrícula.')

        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('alunos/form.html', aluno=aluno, form=request.form)

        for k, v in dados.items():
            setattr(aluno, k, v)

        # Foto nova
        foto = request.files.get('foto')
        if foto and foto.filename:
            caminho, erro_foto = salvar_foto(foto, aluno.id)
            if erro_foto:
                flash(erro_foto, 'warning')
            else:
                aluno.foto = caminho

        log = LogAluno(aluno_id=aluno.id, usuario_id=current_user.id,
                       acao='editou', descricao=f'Dados do aluno atualizados por {current_user.nome}.')
        db.session.add(log)
        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('alunos.perfil', id=aluno.id))

    def _v(val):
        if val is None or str(val) == 'None':
            return ''
        return str(val)

    return render_template('alunos/form.html', aluno=aluno, form={
        'nome': _v(aluno.nome),
        'cpf': _v(aluno.cpf),
        'telefone': _v(aluno.telefone),
        'email': _v(aluno.email),
        'data_nascimento': aluno.data_nascimento.strftime('%Y-%m-%d') if aluno.data_nascimento else '',
        'matricula': _v(aluno.matricula),
        'nivel': _v(aluno.nivel),
        'curso': _v(aluno.curso),
        'serie': _v(aluno.serie),
        'turma': _v(aluno.turma),
        'turno': _v(aluno.turno),
        'responsavel_nome': _v(aluno.responsavel_nome),
        'tipo_contato': aluno.tipo_contato or 'emergencia',
        'responsavel_parentesco': _v(aluno.responsavel_parentesco),
        'responsavel_cpf': _v(aluno.responsavel_cpf),
        'responsavel_contato': _v(aluno.responsavel_contato),
        'responsavel_email': _v(aluno.responsavel_email),
    })


@aluno_bp.route('/perfil/<int:id>')
@login_required
def perfil(id):
    aluno = Aluno.query.get_or_404(id)
    return render_template('alunos/perfil.html', aluno=aluno)


@aluno_bp.route('/busca-json')
@login_required
def busca_json():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    from sqlalchemy import or_
    alunos = Aluno.query.filter(
        or_(
            Aluno.nome.ilike(f'%{q}%'),
            Aluno.matricula.ilike(f'%{q}%')
        )
    ).order_by(Aluno.ativo.desc(), Aluno.nome).limit(10).all()
    return jsonify([{
        'id': a.id,
        'nome': a.nome,
        'matricula': a.matricula or '—',
        'nivel': {'tecnico': 'Técnico', 'graduacao': 'Graduação', 'pos': 'Pós-graduação'}.get(a.nivel or '', a.nivel or ''),
        'curso': a.curso or '',
        'serie': a.serie_completa,
        'foto': a.foto or '',
        'ativo': a.ativo,
    } for a in alunos])


@aluno_bp.route('/desativar/<int:id>', methods=['POST'])
@login_required
def desativar(id):
    from app.utils import apenas_admin
    aluno = Aluno.query.get_or_404(id)
    aluno.ativo = not aluno.ativo
    acao = 'reativou' if aluno.ativo else 'desativou'
    status = 'reativado' if aluno.ativo else 'desativado'
    log = LogAluno(aluno_id=aluno.id, usuario_id=current_user.id,
                   acao=acao, descricao=f'Aluno {status} por {current_user.nome}.')
    db.session.add(log)
    db.session.commit()
    flash(f'Aluno {aluno.nome} {status} com sucesso.', 'success')
    return redirect(url_for('alunos.perfil', id=aluno.id))
