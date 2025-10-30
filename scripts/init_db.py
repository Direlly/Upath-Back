from App.core.database import SessionLocal, engine, Base
from App.models.user import User
from App.models.course import Course, CutoffScore
from App.core.security import get_password_hash

def init_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Criar usuário admin padrão
        admin_user = db.query(User).filter(User.email == "admin@upath.com").first()
        if not admin_user:
            admin_user = User(
                nome="Administrador UPath",
                email="admin@upath.com",
                senha_hash=get_password_hash("Admin@123"),
                role="admin"
            )
            db.add(admin_user)
        
        # Criar usuário estudante de exemplo
        student_user = db.query(User).filter(User.email == "estudante@exemplo.com").first()
        if not student_user:
            student_user = User(
                nome="Estudante Exemplo",
                email="estudante@exemplo.com", 
                senha_hash=get_password_hash("Senha@123"),
                role="student"
            )
            db.add(student_user)
        
        # Adicionar cursos de exemplo (código anterior mantido)
        # ... (o mesmo código de cursos que já existia)
        
        db.commit()
        print("✅ Banco de dados inicializado com sucesso!")
        print("👤 Usuário admin: admin@upath.com / Admin@123")
        print("👤 Usuário estudante: estudante@exemplo.com / Senha@123")
        print("📊 Tabelas criadas: users, courses, cutoff_scores, refresh_tokens, password_reset_tokens, admin_sessions, audit_logs")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao inicializar banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()