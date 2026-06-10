from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
from app import db
from datetime import datetime, timezone

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user     = Usuario.query.filter_by(email=email).first()

        if user and user.ativo and user.check_password(password):
            login_user(user)
            user.ultimo_login = datetime.now(timezone.utc)
            db.session.commit()
            return redirect(url_for('main.dashboard'))
        flash('E-mail ou senha inválidos.', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    from app import db
    from app.models.aluno import formatar_telefone, limpar_numeros
    import os, time
    if request.method == 'POST':
        current_user.nome  = request.form.get('nome', '').strip()
        current_user.cargo = request.form.get('cargo', '').strip() or None
        current_user.ramal = request.form.get('ramal', '').strip() or None

        # Foto de perfil
        foto = request.files.get('foto')
        if foto and foto.filename:
            ext = foto.filename.rsplit('.', 1)[-1].lower()
            if ext in {'jpg', 'jpeg', 'png', 'webp'}:
                if foto.content_length and foto.content_length > 5 * 1024 * 1024:
                    flash('A foto deve ter no máximo 5MB.', 'danger')
                    return render_template('auth/perfil.html')
                pasta = os.path.join(current_app.root_path, 'static', 'uploads', 'avatares')
                os.makedirs(pasta, exist_ok=True)
                nome_arquivo = f'user_{current_user.id}_{int(time.time())}.{ext}'
                foto.save(os.path.join(pasta, nome_arquivo))
                current_user.foto = f'uploads/avatares/{nome_arquivo}'
            else:
                flash('Formato inválido. Use JPG, PNG ou WEBP.', 'danger')
                return render_template('auth/perfil.html')

        tel_raw = request.form.get('telefone', '').strip()
        if tel_raw:
            nums = limpar_numeros(tel_raw)
            if len(nums) in (10, 11):
                current_user.telefone = formatar_telefone(tel_raw)
            else:
                flash('Telefone deve ter 10 ou 11 dígitos com DDD.', 'danger')
                return render_template('auth/perfil.html')
        else:
            current_user.telefone = None

        # Troca de senha opcional
        nova_senha = request.form.get('nova_senha', '').strip()
        senha_atual = request.form.get('senha_atual', '').strip()
        if nova_senha:
            if not current_user.check_password(senha_atual):
                flash('Senha atual incorreta.', 'danger')
                return render_template('auth/perfil.html')
            if len(nova_senha) < 6:
                flash('A nova senha deve ter pelo menos 6 caracteres.', 'danger')
                return render_template('auth/perfil.html')
            current_user.set_password(nova_senha)
            flash('Senha alterada com sucesso!', 'success')

        db.session.commit()
        flash('Perfil atualizado!', 'success')
        return redirect(url_for('auth.perfil'))

    return render_template('auth/perfil.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
