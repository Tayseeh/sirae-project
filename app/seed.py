# seed.py
from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    db.create_all()
    
    # Criar usuário de teste
    if not Usuario.query.filter_by(email='admin@email.com').first():
        admin = Usuario(
            email='admin@email.com',
            nome='Administrador',
            perfil='admin'
        )
        admin.set_password('123456')
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário criado: admin@email.com / 123456")
    else:
        print("✅ Usuário já existe")
    
    print("✅ Banco de dados configurado!")