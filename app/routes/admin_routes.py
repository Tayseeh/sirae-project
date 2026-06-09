from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.usuario import Usuario
from app.models.ocorrencia import LogAuditoria
from app.models.log_admin import LogAdmin
from app.utils import apenas_admin
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

PERFIS_VALIDOS = ('atendente', 'coordenacao', 'pedagogia', 'admin')


def _log_admin(acao, alvo_nome, descricao):
    db.session.add(LogAdmin(
        usuario_id=current_user.id,
        acao=acao,
        alvo_nome=alvo_nome,
        descricao=descricao
    ))


@admin_bp.route('/usuarios')
@login_required
@apenas_admin
def usuarios():
    lista = Usuario.query.order_by(Usuario.perfil, Usuario.nome).all()
    return render_template('admin/usuarios.html', usuarios=lista)


@admin_bp.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
@apenas_admin
def novo_usuario():
    if request.method == 'POST':
        nome   = request.form.get('nome', '').strip()
        email  = request.form.get('email', '').strip()
        perfil = request.form.get('perfil', '').strip()
        senha  = request.form.get('senha', '').strip()

        if not all([nome, email, perfil, senha]):
            flash('Preencha todos os campos.', 'danger')
            return render_template('admin/form_usuario.html', usuario=None)

        if perfil not in PERFIS_VALIDOS:
            flash('Perfil inválido.', 'danger')
            return render_template('admin/form_usuario.html', usuario=None)

        if Usuario.query.filter_by(email=email).first():
            flash('Já existe um usuário com este e-mail.', 'danger')
            return render_template('admin/form_usuario.html', usuario=None)

        u = Usuario(
            nome=nome, email=email, perfil=perfil,
            cargo=request.form.get('cargo','').strip() or None,
            telefone=request.form.get('telefone','').strip() or None,
            ramal=request.form.get('ramal','').strip() or None,
        )
        u.set_password(senha)
        db.session.add(u)
        db.session.flush()
        _log_admin('criou_usuario', nome,
                   f'Usuário "{nome}" ({perfil}) criado por {current_user.nome}. E-mail: {email}')
        db.session.commit()
        flash(f'Usuário {nome} criado com sucesso!', 'success')
        return redirect(url_for('admin.usuarios'))

    return render_template('admin/form_usuario.html', usuario=None)


@admin_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@apenas_admin
def editar_usuario(id):
    u = Usuario.query.get_or_404(id)

    if u.id == current_user.id:
        flash('Use as configurações de perfil para editar seus próprios dados.', 'warning')
        return redirect(url_for('admin.usuarios'))

    if request.method == 'POST':
        perfil_anterior = u.perfil
        u.nome     = request.form.get('nome', '').strip()
        u.email    = request.form.get('email', '').strip()
        u.perfil   = request.form.get('perfil', '').strip()
        u.cargo    = request.form.get('cargo', '').strip() or None
        u.telefone = request.form.get('telefone', '').strip() or None
        u.ramal    = request.form.get('ramal', '').strip() or None
        nova_senha = request.form.get('senha', '').strip()
        senha_alterada = bool(nova_senha)
        if nova_senha:
            u.set_password(nova_senha)

        desc = f'Usuário "{u.nome}" editado por {current_user.nome}.'
        if u.perfil != perfil_anterior:
            desc += f' Perfil: {perfil_anterior} → {u.perfil}.'
        if senha_alterada:
            desc += ' Senha alterada.'

        _log_admin('editou_usuario', u.nome, desc)
        db.session.commit()
        flash('Usuário atualizado!', 'success')
        return redirect(url_for('admin.usuarios'))

    return render_template('admin/form_usuario.html', usuario=u)


@admin_bp.route('/usuarios/desativar/<int:id>')
@login_required
@apenas_admin
def desativar_usuario(id):
    u = Usuario.query.get_or_404(id)
    if u.perfil == 'admin':
        flash('Não é possível desativar um administrador.', 'warning')
    else:
        u.ativo = False
        _log_admin('desativou_usuario', u.nome,
                   f'Usuário "{u.nome}" ({u.perfil}) desativado por {current_user.nome}.')
        db.session.commit()
        flash(f'Usuário {u.nome} desativado.', 'success')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/reativar/<int:id>')
@login_required
@apenas_admin
def reativar_usuario(id):
    u = Usuario.query.get_or_404(id)
    u.ativo = True
    _log_admin('reativou_usuario', u.nome,
               f'Usuário "{u.nome}" ({u.perfil}) reativado por {current_user.nome}.')
    db.session.commit()
    flash(f'Usuário {u.nome} reativado com sucesso!', 'success')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/excluir/<int:id>')
@login_required
@apenas_admin
def excluir_usuario(id):
    u = Usuario.query.get_or_404(id)
    if u.id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect(url_for('admin.usuarios'))
    nome = u.nome
    _log_admin('excluiu_usuario', nome,
               f'Usuário "{nome}" ({u.perfil}) excluído permanentemente por {current_user.nome}.')
    db.session.delete(u)
    db.session.commit()
    flash(f'Usuário {nome} excluído permanentemente.', 'success')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/logs')
@login_required
@apenas_admin
def logs():
    filtro_tipo = request.args.get('tipo', 'ocorrencias')  # ocorrencias | admin

    if filtro_tipo == 'admin':
        registros = LogAdmin.query.order_by(LogAdmin.data_hora.desc()).limit(200).all()
    else:
        filtro_acao = request.args.get('acao', '').strip()
        query = LogAuditoria.query
        if filtro_acao:
            query = query.filter(LogAuditoria.acao == filtro_acao)
        registros = query.order_by(LogAuditoria.data_hora.desc()).limit(200).all()

    acoes_occ = db.session.query(LogAuditoria.acao).distinct().all()
    acoes_occ = [a[0] for a in acoes_occ]

    return render_template('admin/logs.html',
                           registros=registros,
                           filtro_tipo=filtro_tipo,
                           filtro_acao=request.args.get('acao', ''),
                           acoes_occ=acoes_occ)
