from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def requer_perfil(*perfis):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.perfil not in perfis:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return wrapped
    return decorator


def apenas_admin(f):
    return requer_perfil('admin')(f)

def apenas_coordenador(f):
    return requer_perfil('coordenacao')(f)

# Atendente + Pedagogo + Coordenação (todos exceto admin)
def nao_admin(f):
    return requer_perfil('atendente', 'coordenacao', 'pedagogia')(f)
