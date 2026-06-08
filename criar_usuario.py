from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    # Criar tabelas
    db.create_all()
    
    # Verificar se já existe
    if not Usuario.query.filter_by(email='admin@email.com').first():
        # Criar usuário admin
        admin = Usuario(
            email='admin@email.com',
            nome='Administrador',
            perfil='admin'
        )
        admin.set_password('123456')
        db.session.add(admin)
        db.session.commit()
        print("=" * 50)
        print("✅ Usuário criado com sucesso!")
        print("   Email: admin@email.com")
        print("   Senha: 123456")
        print("=" * 50)
    else:
        print("=" * 50)
        print("✅ Usuário já existe!")
        print("   Email: admin@email.com")
        print("=" * 50)
    
    # Listar todos os usuários
    usuarios = Usuario.query.all()
    print(f"\n📋 Total de usuários no sistema: {len(usuarios)}")
    for u in usuarios:
        print(f"   - {u.email} ({u.nome}) - Perfil: {u.perfil}")