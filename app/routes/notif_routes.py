from flask import Blueprint, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.models.notificacao import Notificacao
from app import db

notif_bp = Blueprint('notif', __name__)


@notif_bp.route('/')
@login_required
def listar():
    """Retorna notificações não lidas do usuário em JSON."""
    notifs = Notificacao.query.filter_by(
        usuario_id=current_user.id, lida=False
    ).order_by(Notificacao.data_hora.desc()).limit(10).all()

    return jsonify([{
        'id': n.id,
        'mensagem': n.mensagem,
        'ocorrencia_id': n.ocorrencia_id,
        'data_hora': n.data_hora.strftime('%d/%m/%Y às %H:%M')
    } for n in notifs])


@notif_bp.route('/marcar-lida/<int:id>')
@login_required
def marcar_lida(id):
    """Marca uma notificação como lida e redireciona para a ocorrência."""
    n = db.session.get(Notificacao, id)
    if n is None:
        return redirect(url_for('main.dashboard'))
    if n.usuario_id != current_user.id:
        return redirect(url_for('main.dashboard'))
    ocorrencia_id = n.ocorrencia_id
    n.lida = True
    db.session.commit()
    return redirect(url_for('main.ver_ocorrencia', id=ocorrencia_id))


@notif_bp.route('/marcar-todas-lidas', methods=['POST'])
@login_required
def marcar_todas_lidas():
    """Marca todas as notificações do usuário como lidas."""
    Notificacao.query.filter_by(
        usuario_id=current_user.id, lida=False
    ).update({'lida': True})
    db.session.commit()
    return jsonify({'ok': True})
