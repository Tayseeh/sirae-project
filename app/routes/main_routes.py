import os
import time
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.ocorrencia import Ocorrencia, LogAuditoria
from app.models.aluno import Aluno
from app.models.usuario import Usuario
from app.utils import nao_admin, apenas_coordenador
from app import db

main_bp = Blueprint('main', __name__)

UPLOAD_EXTS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
MAX_UPLOAD_MB = 5


def _log(ocorrencia_id, acao, descricao, sigiloso=False, anexo_log=None):
    db.session.add(LogAuditoria(
        ocorrencia_id=ocorrencia_id,
        usuario_id=current_user.id,
        acao=acao,
        descricao_acao=descricao,
        sigiloso=sigiloso,
        anexo_log=anexo_log,
    ))


def _salvar_anexo_log(usuario_id):
    """Salva anexo de andamento/encaminhamento/encerramento. Retorna nome do arquivo ou None."""
    arquivo = request.files.get('anexo_log')
    if not arquivo or not arquivo.filename:
        return None
    ext = arquivo.filename.rsplit('.', 1)[-1].lower()
    if ext not in UPLOAD_EXTS:
        flash('Formato de anexo não permitido. Use PDF, JPG, PNG, DOC ou DOCX.', 'warning')
        return None
    # Verificação de tamanho (lê em memória para checar antes de salvar)
    arquivo.seek(0, 2)
    tamanho = arquivo.tell()
    arquivo.seek(0)
    if tamanho > MAX_UPLOAD_MB * 1024 * 1024:
        flash(f'O anexo deve ter no máximo {MAX_UPLOAD_MB}MB.', 'warning')
        return None
    pasta = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(pasta, exist_ok=True)
    nome_seguro = secure_filename(arquivo.filename)
    nome = f"{usuario_id}_{int(time.time())}_{nome_seguro}"
    arquivo.save(os.path.join(pasta, nome))
    return nome


@main_bp.route('/')
@login_required
def dashboard():
    if current_user.perfil == 'admin':
        return redirect(url_for('admin.usuarios'))

    filtro_nome   = request.args.get('nome', '').strip()
    filtro_tipo   = request.args.get('tipo', '').strip()
    filtro_status = request.args.get('status', '').strip()
    filtro_resp   = request.args.get('responsavel', '').strip()

    filtro_aplicado = any([filtro_nome, filtro_tipo, filtro_status, filtro_resp])

    # Padrão: painel do próprio usuário, abertas + em andamento
    if not filtro_aplicado:
        filtro_resp   = str(current_user.id)
        filtro_status = 'ativas'

    # Se status selecionado sem responsável → aplica ao usuário logado
    if filtro_status and not filtro_resp and not filtro_nome and not filtro_tipo:
        filtro_resp = str(current_user.id)

    # Resolve o usuário do contexto
    u_ctx = db.session.get(Usuario, int(filtro_resp)) if filtro_resp else None

    # Nome e subtítulo do painel
    if u_ctx and u_ctx.id == current_user.id:
        nome_contexto      = current_user.nome.split()[0]
        subtitulo_contexto = 'Suas ocorrências no setor de apoio.'
    elif u_ctx:
        nome_contexto      = u_ctx.nome.split()[0]
        subtitulo_contexto = f'Ocorrências sob responsabilidade de {u_ctx.nome}.'
    else:
        nome_contexto      = 'todos'
        subtitulo_contexto = 'Visão geral de todos os registros do setor de apoio.'

    # Total do usuário do contexto (todas, sem filtro de status)
    q_usuario = Ocorrencia.query
    if u_ctx:
        q_usuario = q_usuario.filter(Ocorrencia.responsavel_id == u_ctx.id)
    total_usuario = q_usuario.count()
    total_geral   = Ocorrencia.query.count()

    # Contadores do contexto (com filtros de nome/tipo aplicados)
    q_ctx = Ocorrencia.query
    if filtro_resp:
        q_ctx = q_ctx.filter(Ocorrencia.responsavel_id == int(filtro_resp))
    if filtro_nome:
        from sqlalchemy import or_
        q_ctx = q_ctx.join(Aluno).filter(
            or_(Aluno.nome.ilike(f'%{filtro_nome}%'),
                Aluno.matricula.ilike(f'%{filtro_nome}%'))
        )
    if filtro_tipo:
        q_ctx = q_ctx.filter(Ocorrencia.tipo == filtro_tipo)
    abertas    = q_ctx.filter(Ocorrencia.status == 'aberta').count()
    acomp      = q_ctx.filter(Ocorrencia.status == 'em_andamento').count()
    encerradas = q_ctx.filter(Ocorrencia.status == 'encerrada').count()
    contexto_label = nome_contexto

    # Query da listagem
    query = Ocorrencia.query
    if filtro_nome:
        from sqlalchemy import or_
        query = query.join(Aluno).filter(
            or_(Aluno.nome.ilike(f'%{filtro_nome}%'),
                Aluno.matricula.ilike(f'%{filtro_nome}%'))
        )
    if filtro_tipo:
        query = query.filter(Ocorrencia.tipo == filtro_tipo)
    if filtro_status == 'ativas':
        query = query.filter(Ocorrencia.status.in_(['aberta', 'em_andamento']))
    elif filtro_status:
        query = query.filter(Ocorrencia.status == filtro_status)
    else:
        query = query.filter(Ocorrencia.status != 'encerrada')
    if filtro_resp:
        query = query.filter(Ocorrencia.responsavel_id == int(filtro_resp))

    # Paginação
    page = request.args.get('page', 1, type=int)
    paginacao = query.order_by(Ocorrencia.data_criacao.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    ocorrencias = paginacao.items

    atendentes = Usuario.query.filter(
        Usuario.perfil.in_(['atendente', 'coordenacao', 'pedagogia']),
        Usuario.ativo == True
    ).order_by(Usuario.nome).all()

    return render_template('dashboard.html',
        ocorrencias=ocorrencias,
        filtro_nome=filtro_nome, filtro_tipo=filtro_tipo,
        filtro_status=filtro_status, filtro_resp=filtro_resp,
        total_usuario=total_usuario, total_geral=total_geral,
        abertas=abertas, acomp=acomp, encerradas=encerradas,
        contexto_label=contexto_label,
        nome_contexto=nome_contexto,
        subtitulo_contexto=subtitulo_contexto,
        atendentes=atendentes,
        paginacao=paginacao)


@main_bp.route('/nova', methods=['GET', 'POST'])
@login_required
@nao_admin
def nova_ocorrencia():
    if request.method == 'POST':
        aluno_id = request.form.get('aluno_id', '').strip()
        tipo     = request.form.get('tipo', '').strip()
        desc     = request.form.get('descricao', '').strip()

        if not aluno_id or not tipo or not desc:
            flash('Preencha todos os campos obrigatórios.', 'danger')
            return render_template('cadastro.html')

        aluno = db.session.get(Aluno, aluno_id)
        if not aluno:
            flash('Aluno não encontrado.', 'danger')
            return render_template('cadastro.html')

        # Upload
        arquivo = request.files.get('anexo')
        nome_arquivo = None
        if arquivo and arquivo.filename:
            ext = arquivo.filename.rsplit('.', 1)[-1].lower()
            if ext not in UPLOAD_EXTS:
                flash('Formato de arquivo não permitido.', 'danger')
                return render_template('cadastro.html')
            arquivo.seek(0, 2)
            tamanho = arquivo.tell()
            arquivo.seek(0)
            if tamanho > MAX_UPLOAD_MB * 1024 * 1024:
                flash(f'O arquivo deve ter no máximo {MAX_UPLOAD_MB}MB.', 'danger')
                return render_template('cadastro.html')
            pasta = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(pasta, exist_ok=True)
            nome_seguro = secure_filename(arquivo.filename)
            nome_arquivo = f"{current_user.id}_{int(time.time())}_{nome_seguro}"
            arquivo.save(os.path.join(pasta, nome_arquivo))

        nova = Ocorrencia(
            aluno_id=int(aluno_id),
            tipo=tipo,
            descricao=desc,
            anexo_arquivo=nome_arquivo,
            criado_por_id=current_user.id,
            responsavel_id=current_user.id,
            status='aberta'
        )
        db.session.add(nova)
        db.session.flush()
        _log(nova.id, 'criada',
             f'Ocorrência criada por {current_user.nome} para o aluno {aluno.nome}')
        db.session.commit()

        flash(f'Ocorrência registrada para {aluno.nome}!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('cadastro.html')


@main_bp.route('/ocorrencia/<int:id>')
@login_required
@nao_admin
def ver_ocorrencia(id):
    ocorrencia = Ocorrencia.query.get_or_404(id)
    # Só quem é responsável atual vê o painel de encaminhar/editar
    e_responsavel = (ocorrencia.responsavel_id == current_user.id)
    opcoes = []
    if e_responsavel and ocorrencia.status != 'encerrada':
        opcoes = Usuario.query.filter(
            Usuario.perfil.in_(['atendente', 'coordenacao', 'pedagogia']),
            Usuario.id != ocorrencia.responsavel_id,
            Usuario.ativo == True
        ).order_by(Usuario.perfil.desc(), Usuario.nome).all()
    return render_template('ocorrencia.html', ocorrencia=ocorrencia,
                           opcoes=opcoes, e_responsavel=e_responsavel)


@main_bp.route('/ocorrencia/<int:id>/encaminhar', methods=['POST'])
@login_required
@nao_admin
def encaminhar_ocorrencia(id):
    ocorrencia = Ocorrencia.query.get_or_404(id)

    if ocorrencia.responsavel_id != current_user.id:
        flash('Apenas o responsável atual pode encaminhar esta ocorrência.', 'danger')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    if ocorrencia.status == 'encerrada':
        flash('Não é possível encaminhar uma ocorrência encerrada.', 'warning')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    novo_resp_id = request.form.get('responsavel_id', '').strip()
    motivo       = request.form.get('motivo', '').strip()

    if not novo_resp_id:
        flash('Selecione para quem encaminhar.', 'danger')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    novo_resp = db.session.get(Usuario, novo_resp_id)
    if not novo_resp:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    anterior = ocorrencia.responsavel.nome
    ocorrencia.responsavel_id = novo_resp.id
    ocorrencia.status = 'em_andamento'

    desc = f'Encaminhada de {anterior} para {novo_resp.nome} ({novo_resp.perfil})'
    if motivo:
        desc += f'. Motivo: {motivo}'

    _log(id, 'encaminhada', desc, anexo_log=_salvar_anexo_log(current_user.id))

    # Cria notificação para o destinatário
    from app.models.notificacao import Notificacao
    db.session.add(Notificacao(
        usuario_id=novo_resp.id,
        ocorrencia_id=id,
        mensagem=f'{current_user.nome} encaminhou a ocorrência #{id:04d} para você.'
    ))

    db.session.commit()

    flash(f'Ocorrência encaminhada para {novo_resp.nome}!', 'success')
    return redirect(url_for('main.ver_ocorrencia', id=id))



@main_bp.route('/ocorrencia/<int:id>/atualizar', methods=['POST'])
@login_required
@nao_admin
def atualizar_ocorrencia(id):
    """Registra andamento sem sobrescrever a descrição original"""
    ocorrencia = Ocorrencia.query.get_or_404(id)

    if ocorrencia.responsavel_id != current_user.id:
        flash('Apenas o responsável atual pode atualizar esta ocorrência.', 'danger')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    if ocorrencia.status == 'encerrada':
        flash('Não é possível atualizar uma ocorrência encerrada.', 'warning')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    andamento = request.form.get('andamento', '').strip()
    sigiloso  = request.form.get('sigiloso') == '1'

    if not andamento:
        flash('Descreva o andamento antes de salvar.', 'danger')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    # Ao registrar andamento, muda automaticamente para Em andamento
    status_anterior = ocorrencia.status
    ocorrencia.status = 'em_andamento'

    desc_log  = f'Andamento registrado por {current_user.nome}: {andamento}'
    anexo_log = _salvar_anexo_log(current_user.id)

    _log(id, 'atualizada', desc_log, sigiloso=sigiloso, anexo_log=anexo_log)
    db.session.commit()

    flash('Andamento registrado com sucesso!', 'success')
    return redirect(url_for('main.ver_ocorrencia', id=id))


@main_bp.route('/ocorrencia/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@nao_admin
def editar_ocorrencia(id):
    ocorrencia = Ocorrencia.query.get_or_404(id)

    if ocorrencia.responsavel_id != current_user.id:
        flash('Apenas o responsável atual pode editar esta ocorrência.', 'danger')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    if ocorrencia.status == 'encerrada':
        flash('Não é possível editar uma ocorrência encerrada.', 'warning')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    if request.method == 'POST':
        tipo_anterior   = ocorrencia.tipo
        status_anterior = ocorrencia.status
        desc_anterior   = ocorrencia.descricao

        novo_tipo   = request.form.get('tipo', '').strip()
        nova_desc   = request.form.get('descricao', '').strip()
        novo_status = request.form.get('status', '').strip()

        ocorrencia.tipo      = novo_tipo
        ocorrencia.descricao = nova_desc
        if novo_status in ['aberta', 'em_andamento']:
            # Impede volta para "aberta" se já existe algum andamento registrado
            tem_andamento = any(
                log.acao in ('atualizada', 'encaminhada')
                for log in ocorrencia.logs
            )
            if novo_status == 'aberta' and tem_andamento:
                flash('Não é possível voltar para "Aberta" após registro de andamentos.', 'warning')
                novo_status = status_anterior
            ocorrencia.status = novo_status

        mudancas = []

        # Remove anexo se solicitado
        remover = request.form.get('remover_anexo', '0')
        if remover == '1' and ocorrencia.anexo_arquivo:
            try:
                caminho = os.path.join(current_app.root_path, 'static', 'uploads', ocorrencia.anexo_arquivo)
                if os.path.exists(caminho):
                    os.remove(caminho)
            except Exception:
                pass
            ocorrencia.anexo_arquivo = None
            mudancas.append('Anexo removido')

        # Novo anexo enviado
        arquivo = request.files.get('anexo')
        if arquivo and arquivo.filename:
            ext = arquivo.filename.rsplit('.', 1)[-1].lower()
            if ext in UPLOAD_EXTS:
                arquivo.seek(0, 2)
                tamanho = arquivo.tell()
                arquivo.seek(0)
                if tamanho > MAX_UPLOAD_MB * 1024 * 1024:
                    flash(f'O arquivo deve ter no máximo {MAX_UPLOAD_MB}MB.', 'danger')
                    return redirect(url_for('main.ver_ocorrencia', id=id))
                pasta = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(pasta, exist_ok=True)
                nome_seguro = secure_filename(arquivo.filename)
                nome_arquivo = f"{current_user.id}_{int(time.time())}_{nome_seguro}"
                arquivo.save(os.path.join(pasta, nome_arquivo))
                ocorrencia.anexo_arquivo = nome_arquivo
                mudancas.append('Anexo atualizado')

        labels = {'aberta': 'Aberta', 'em_andamento': 'Em andamento'}
        if novo_tipo != tipo_anterior:
            mudancas.append(f'Tipo: "{tipo_anterior}" → "{novo_tipo}"')
        if novo_status and novo_status != status_anterior and novo_status in ['aberta', 'em_andamento']:
            mudancas.append(f'Status: "{labels.get(status_anterior)}" → "{labels.get(novo_status)}"')
        if nova_desc != desc_anterior:
            mudancas.append('Descrição atualizada')

        desc_log = f'Editada por {current_user.nome}.'
        if mudancas:
            desc_log += ' Alterações: ' + ' | '.join(mudancas)

        _log(id, 'atualizada', desc_log)
        db.session.commit()
        flash('Ocorrência atualizada!', 'success')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    # GET: redireciona para a tela da ocorrência (edição agora é inline)
    return redirect(url_for('main.ver_ocorrencia', id=id))


@main_bp.route('/ocorrencia/<int:id>/encerrar', methods=['GET', 'POST'])
@login_required
@nao_admin
def encerrar_ocorrencia(id):
    ocorrencia = Ocorrencia.query.get_or_404(id)

    if ocorrencia.responsavel_id != current_user.id:
        flash('Apenas o responsável atual pode encerrar esta ocorrência.', 'danger')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    if ocorrencia.status == 'encerrada':
        flash('Esta ocorrência já está encerrada.', 'warning')
        return redirect(url_for('main.ver_ocorrencia', id=id))

    if request.method == 'POST':
        resolucao = request.form.get('resolucao', '').strip()
        if not resolucao:
            flash('Descreva a resolução antes de encerrar.', 'danger')
            return redirect(url_for('main.ver_ocorrencia', id=id))

        sigiloso  = request.form.get('sigiloso') == '1'
        anexo_log = _salvar_anexo_log(current_user.id)

        ocorrencia.encerrar()
        _log(id, 'encerrada',
             f'Encerrada por {current_user.nome} em {ocorrencia.data_encerramento.strftime("%d/%m/%Y às %H:%M")}. '
             f'Resolução: {resolucao}',
             sigiloso=sigiloso, anexo_log=anexo_log)
        db.session.commit()
        flash(f'Ocorrência #{id} encerrada!', 'success')
        return redirect(url_for('main.dashboard'))

    return redirect(url_for('main.ver_ocorrencia', id=id))









@main_bp.route('/anexo/<path:filename>')
@login_required
@nao_admin
def ver_anexo(filename):
    """Serve arquivos de anexo das ocorrências"""
    pasta = os.path.join(current_app.root_path, 'static', 'uploads')
    return send_from_directory(pasta, filename)


@main_bp.route('/relatorios/exportar')
@login_required
@apenas_coordenador
def exportar_relatorio():
    from sqlalchemy import func
    from datetime import datetime

    filtro_tipo = request.args.get('tipo', '').strip()
    tipo_filter = (Ocorrencia.tipo == filtro_tipo,) if filtro_tipo else ()

    ocorrencias_filtradas = Ocorrencia.query.filter(*tipo_filter)        .order_by(Ocorrencia.data_criacao.desc()).all() if filtro_tipo else []

    por_tipo_geral = db.session.query(
        Ocorrencia.tipo, func.count(Ocorrencia.id)
    ).group_by(Ocorrencia.tipo).order_by(func.count(Ocorrencia.id).desc()).all()

    por_status = db.session.query(
        Ocorrencia.status, func.count(Ocorrencia.id)
    ).filter(*tipo_filter).group_by(Ocorrencia.status).all()

    por_atendente = db.session.query(
        Usuario.nome, func.count(Ocorrencia.id)
    ).join(Ocorrencia, Ocorrencia.responsavel_id == Usuario.id)     .filter(*tipo_filter).group_by(Usuario.id, Usuario.nome).all()

    por_aluno = db.session.query(
        Aluno.nome, func.count(Ocorrencia.id)
    ).join(Ocorrencia).filter(*tipo_filter)     .group_by(Aluno.id, Aluno.nome)     .order_by(func.count(Ocorrencia.id).desc()).limit(10).all()

    total      = Ocorrencia.query.filter(*tipo_filter).count()
    encerradas = Ocorrencia.query.filter(Ocorrencia.status == 'encerrada', *tipo_filter).count()
    taxa       = int((encerradas / total * 100)) if total else 0

    return render_template('relatorio_print.html',
        por_tipo_geral=por_tipo_geral, por_status=por_status,
        por_atendente=por_atendente, por_aluno=por_aluno,
        total=total, encerradas=encerradas, taxa=taxa,
        filtro_tipo=filtro_tipo,
        ocorrencias_filtradas=ocorrencias_filtradas,
        gerado_em=datetime.now().strftime('%d/%m/%Y às %H:%M'))


@main_bp.route('/relatorios')
@login_required
@apenas_coordenador
def relatorios():
    from sqlalchemy import func
    from app.models.usuario import Usuario as U

    filtro_tipo = request.args.get('tipo', '').strip()
    tipo_filter = (Ocorrencia.tipo == filtro_tipo,) if filtro_tipo else ()

    # Ocorrências filtradas para listagem
    ocorrencias_filtradas = Ocorrencia.query.filter(*tipo_filter)\
        .order_by(Ocorrencia.data_criacao.desc()).all() if filtro_tipo else []

    # Tipos — sempre geral para o gráfico de barras
    por_tipo_geral = db.session.query(
        Ocorrencia.tipo, func.count(Ocorrencia.id)
    ).group_by(Ocorrencia.tipo).order_by(func.count(Ocorrencia.id).desc()).all()

    # Demais — filtrados
    por_status = db.session.query(
        Ocorrencia.status, func.count(Ocorrencia.id)
    ).filter(*tipo_filter).group_by(Ocorrencia.status).all()

    por_atendente = db.session.query(
        U.nome, func.count(Ocorrencia.id)
    ).join(Ocorrencia, Ocorrencia.responsavel_id == U.id)\
     .filter(*tipo_filter).group_by(U.id, U.nome)\
     .order_by(func.count(Ocorrencia.id).desc()).all()

    por_aluno = db.session.query(
        Aluno.nome, func.count(Ocorrencia.id)
    ).join(Ocorrencia).filter(*tipo_filter)\
     .group_by(Aluno.id, Aluno.nome)\
     .order_by(func.count(Ocorrencia.id).desc()).limit(10).all()

    total      = Ocorrencia.query.filter(*tipo_filter).count()
    encerradas = Ocorrencia.query.filter(Ocorrencia.status == 'encerrada', *tipo_filter).count()
    taxa       = int((encerradas / total * 100)) if total else 0

    return render_template('relatorios.html',
        por_tipo_geral=por_tipo_geral, por_status=por_status,
        por_atendente=por_atendente, por_aluno=por_aluno,
        total=total, encerradas=encerradas, taxa=taxa,
        filtro_tipo=filtro_tipo,
        ocorrencias_filtradas=ocorrencias_filtradas)
