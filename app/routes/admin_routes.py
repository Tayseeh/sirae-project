from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models.usuario import Usuario
from app.models.ocorrencia import LogAuditoria
from app.utils import apenas_admin
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


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

        if perfil not in ('atendente', 'coordenacao'):
            flash('Perfil inválido.', 'danger')
            return render_template('admin/form_usuario.html', usuario=None)

        if Usuario.query.filter_by(email=email).first():
            flash('Já existe um usuário com este e-mail.', 'danger')
            return render_template('admin/form_usuario.html', usuario=None)

        u = Usuario(nome=nome, email=email, perfil=perfil)
        u.set_password(senha)
        db.session.add(u)
        db.session.commit()
        flash(f'Usuário {nome} criado com sucesso!', 'success')
        return redirect(url_for('admin.usuarios'))

    return render_template('admin/form_usuario.html', usuario=None)


@admin_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@apenas_admin
def editar_usuario(id):
    u = Usuario.query.get_or_404(id)

    if u.perfil == 'admin':
        flash('Não é possível editar outro administrador.', 'warning')
        return redirect(url_for('admin.usuarios'))

    if request.method == 'POST':
        u.nome   = request.form.get('nome', '').strip()
        u.email  = request.form.get('email', '').strip()
        u.perfil = request.form.get('perfil', '').strip()
        nova_senha = request.form.get('senha', '').strip()
        if nova_senha:
            u.set_password(nova_senha)
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
        db.session.commit()
        flash(f'Usuário {u.nome} desativado.', 'success')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/logs')
@login_required
@apenas_admin
def logs():
    page = request.args.get('page', 1, type=int)
    filtro_acao = request.args.get('acao', '').strip()

    query = LogAuditoria.query
    if filtro_acao:
        query = query.filter(LogAuditoria.acao == filtro_acao)

    logs_pag = query.order_by(LogAuditoria.data_hora.desc()).limit(200).all()
    acoes = db.session.query(LogAuditoria.acao).distinct().all()
    acoes = [a[0] for a in acoes]

    return render_template('admin/logs.html', logs=logs_pag,
                           acoes=acoes, filtro_acao=filtro_acao)
