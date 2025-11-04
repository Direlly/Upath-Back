from sqlalchemy.orm import Session
from App.models.curso import Course, CutoffScore, Scholarship
from schemas.course import CourseCreate, CutoffUpdate, ScholarshipCreate
from datetime import datetime

class CourseService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_courses(self, filters: dict = None) -> list:
        query = self.db.query(Course).filter(Course.is_active == True)
        
        if filters:
            if filters.get('q'):
                query = query.filter(Course.nome.ilike(f"%{filters['q']}%"))
            if filters.get('estado'):
                query = query.filter(Course.estado == filters['estado'])
            if filters.get('area'):
                query = query.filter(Course.area == filters['area'])
        
        return query.all()
    
    def get_course_by_id(self, course_id: int) -> Course:
        return self.db.query(Course).filter(Course.id == course_id).first()
    
    def create_course(self, course_data: CourseCreate) -> Course:
        # Determinar tipo de instituição baseado no valor
        tipo_instituicao = "privada" if course_data.valor > 0 else "publica"
        
        course = Course(
            **course_data.dict(),
            tipo_instituicao=tipo_instituicao
        )
        
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def update_course(self, course_id: int, course_data: CourseCreate) -> Course:
        course = self.get_course_by_id(course_id)
        if not course:
            return None
        
        for field, value in course_data.dict().items():
            setattr(course, field, value)
        
        # Atualizar tipo de instituição
        course.tipo_instituicao = "privada" if course_data.valor > 0 else "publica"
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def delete_course(self, course_id: int) -> bool:
        course = self.get_course_by_id(course_id)
        if not course:
            return False
        
        # Soft delete
        course.is_active = False
        self.db.commit()
        return True
    
    def update_cutoff_score(self, cutoff_data: CutoffUpdate, admin_name: str) -> bool:
        try:
            cutoff = CutoffScore(
                instituicao=cutoff_data.nome_instituicao,
                nome_curso=cutoff_data.nome_curso,
                estado=cutoff_data.estado,
                modalidade=cutoff_data.modalidade,
                ano=cutoff_data.ano,
                nota_corte=cutoff_data.nova_nota_corte,
                updated_by=admin_name
            )
            
            self.db.add(cutoff)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
    
    def get_last_cutoff_update(self) -> CutoffScore:
        return self.db.query(CutoffScore).order_by(CutoffScore.updated_at.desc()).first()
    
    def add_scholarship(self, course_id: int, scholarship_data: ScholarshipCreate) -> bool:
        course = self.get_course_by_id(course_id)
        if not course or course.valor == 0:
            return False  # Só privadas podem ter bolsa
        
        scholarship = Scholarship(
            curso_id=course_id,
            programa=scholarship_data.programa,
            percentual_desconto=scholarship_data.percentual_desconto
        )
        
        self.db.add(scholarship)
        self.db.commit()
        return True
    
    def remove_scholarship(self, course_id: int) -> bool:
        scholarship = self.db.query(Scholarship).filter(
            Scholarship.curso_id == course_id
        ).first()
        
        if scholarship:
            self.db.delete(scholarship)
            self.db.commit()
            return True
        return False