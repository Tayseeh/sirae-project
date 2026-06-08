import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models.ocorrencia import Ocorrencia
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    ocorrencias = Ocorrencia.query.all()
    return render_template('dashboard.html', ocorrencias=ocorrencias)

@main_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova_ocorrencia():
    if request.method == 'POST':
        aluno = request.form.get('aluno_nome')
        tipo = request.form.get('tipo')
        desc = request.form.get('descricao')
        
        # Lógica de Upload (RF06)
        arquivo = request.files.get('anexo')
        nome_arquivo = None
        
        if arquivo and arquivo.filename != '':
            pasta_uploads = os.path.join(current_app.root_path, 'static', 'uploads')
            if not os.path.exists(pasta_uploads):
                os.makedirs(pasta_uploads)
            
            nome_arquivo = arquivo.filename
            caminho_salvar = os.path.join(pasta_uploads, nome_arquivo)
            arquivo.save(caminho_salvar)

        nova = Ocorrencia(
            aluno_nome=aluno,
            tipo=tipo,
            descricao=desc,
            anexo_arquivo=nome_arquivo,
            responsavel_id=current_user.id # Rastreabilidade (RNF04)
        )
        db.session.add(nova)
        db.session.commit()
        flash('Ocorrência registrada com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('cadastro.html')

@main_bp.route('/encerrar/<int:id>')
@login_required
def encerrar_ocorrencia(id):
    """Rota para RF04 - Encerramento"""
    ocorrencia = Ocorrencia.query.get_or_404(id)
    ocorrencia.encerrar() # Chama o método da classe POO
    flash(f'Ocorrência #{id} foi encerrada.', 'success')
    return redirect(url_for('main.dashboard'))