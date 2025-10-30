from core.database import SessionLocal, engine, Base
from models.user import User
from models.course import Course, CutoffScore
from core.security import get_password_hash

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
        
        # Adicionar alguns cursos de exemplo
        if db.query(Course).count() == 0:
            sample_courses = [
                Course(
                    nome="Medicina",
                    area="Saúde",
                    instituicao="UFPE",
                    estado="PE",
                    duracao_anos=6,
                    valor=0.0,
                    tipo_instituicao="publica"
                ),
                Course(
                    nome="Engenharia Civil",
                    area="Exatas",
                    instituicao="UFPE", 
                    estado="PE",
                    duracao_anos=5,
                    valor=0.0,
                    tipo_instituicao="publica"
                ),
                Course(
                    nome="Administração",
                    area="Humanas", 
                    instituicao="Faculdade XYZ",
                    estado="SP",
                    duracao_anos=4,
                    valor=950.0,
                    tipo_instituicao="privada"
                ),
                Course(
                    nome="Psicologia",
                    area="Humanas",
                    instituicao="Universidade ABC",
                    estado="RJ", 
                    duracao_anos=5,
                    valor=1200.0,
                    tipo_instituicao="privada"
                ),
                Course(
                    nome="Ciência da Computação",
                    area="Exatas",
                    instituicao="UFMG",
                    estado="MG",
                    duracao_anos=4,
                    valor=0.0,
                    tipo_instituicao="publica" 
                )
            ]
            db.add_all(sample_courses)
        
        # Adicionar notas de corte de exemplo
        if db.query(CutoffScore).count() == 0:
            sample_cutoffs = [
                CutoffScore(
                    instituicao="UFPE",
                    nome_curso="Medicina",
                    estado="PE",
                    modalidade="ampla",
                    ano=2024,
                    nota_corte=830.5,
                    updated_by="Sistema"
                ),
                CutoffScore(
                    instituicao="UFPE",
                    nome_curso="Engenharia Civil",
                    estado="PE", 
                    modalidade="ampla",
                    ano=2024,
                    nota_corte=710.2,
                    updated_by="Sistema"
                ),
                CutoffScore(
                    instituicao="UFMG",
                    nome_curso="Ciência da Computação",
                    estado="MG",
                    modalidade="ampla", 
                    ano=2024,
                    nota_corte=780.8,
                    updated_by="Sistema"
                ),
                CutoffScore(
                    instituicao="Universidade ABC",
                    nome_curso="Psicologia", 
                    estado="RJ",
                    modalidade="ampla",
                    ano=2024,
                    nota_corte=650.3,
                    updated_by="Sistema"
                )
            ]
            db.add_all(sample_cutoffs)
        
        db.commit()
        print("✅ Banco de dados inicializado com sucesso!")
        print("👤 Usuário admin: admin@upath.com / Admin@123")
        print("👤 Usuário estudante: estudante@exemplo.com / Senha@123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao inicializar banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()