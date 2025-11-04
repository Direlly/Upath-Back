from sqlalchemy.orm import Session
from App.models.teste import VocationalTest, TestQuestion, SuggestedCourse
from schemas.test import TestStart, TestAnswer, TestFinish
from datetime import datetime
import requests
from core.config import settings

class TestService:
    def __init__(self, db: Session):
        self.db = db
    
    def start_test(self, user_id: int, test_data: TestStart) -> VocationalTest:
        test = VocationalTest(
            user_id=user_id,
            test_name=test_data.nome_teste,
            mode=test_data.modo,
            status="in_progress"
        )
        
        self.db.add(test)
        self.db.commit()
        self.db.refresh(test)
        
        # Criar perguntas iniciais
        questions = [
            "Você prefere trabalhar com números ou com pessoas?",
            "Gosta de atividades ao ar livre?",
            "Prefere rotina estabelecida ou desafios novos?",
            "Tem facilidade com tecnologia?",
            "Gosta de ajudar outras pessoas?",
            "Prefere trabalhar sozinho ou em equipe?",
            "Tem interesse por ciências?",
            "Gosta de atividades criativas?"
        ]
        
        for i, question_text in enumerate(questions, 1):
            question = TestQuestion(
                test_id=test.id,
                question_text=question_text,
                question_order=i
            )
            self.db.add(question)
        
        self.db.commit()
        return test
    
    def save_answer(self, answer_data: TestAnswer) -> bool:
        question = self.db.query(TestQuestion).filter(
            TestQuestion.id == answer_data.pergunta_id,
            TestQuestion.test_id == answer_data.test_id
        ).first()
        
        if question:
            question.answer = answer_data.resposta
            self.db.commit()
            return True
        return False
    
    def finish_test(self, test_id: int) -> VocationalTest:
        test = self.db.query(VocationalTest).filter(VocationalTest.id == test_id).first()
        if not test:
            return None
        
        # Buscar respostas
        questions = self.db.query(TestQuestion).filter(
            TestQuestion.test_id == test_id
        ).order_by(TestQuestion.question_order).all()
        
        # Preparar dados para IA
        answers = [q.answer for q in questions if q.answer]
        
        try:
            # Integração com serviço de IA
            ia_response = requests.post(
                f"{settings.AI_SERVICE_URL}/predict",
                json={"respostas": answers}
            )
            
            if ia_response.status_code == 200:
                ia_data = ia_response.json()
                test.area_conhecimento = ia_data["area_predita"]
                test.confidence_score = ia_data["confianca"]
                
                # Salvar cursos sugeridos
                for curso_nome in ia_data["cursos_sugeridos"]:
                    suggested_course = SuggestedCourse(
                        test_id=test.id,
                        course_name=curso_nome
                    )
                    self.db.add(suggested_course)
        
        except requests.RequestException:
            # Fallback se IA não estiver disponível
            test.area_conhecimento = "Ciências Humanas"
            default_courses = ["Psicologia", "História", "Sociologia", "Jornalismo"]
            for curso_nome in default_courses:
                suggested_course = SuggestedCourse(
                    test_id=test.id,
                    course_name=curso_nome
                )
                self.db.add(suggested_course)
        
        test.status = "completed"
        test.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(test)
        
        return test
    
    def get_user_tests(self, user_id: int) -> list:
        return self.db.query(VocationalTest).filter(
            VocationalTest.user_id == user_id
        ).order_by(VocationalTest.created_at.desc()).all()
    
    def get_test_details(self, test_id: int, user_id: int) -> dict:
        test = self.db.query(VocationalTest).filter(
            VocationalTest.id == test_id,
            VocationalTest.user_id == user_id
        ).first()
        
        if not test:
            return None
        
        questions = self.db.query(TestQuestion).filter(
            TestQuestion.test_id == test_id
        ).order_by(TestQuestion.question_order).all()
        
        suggested_courses = self.db.query(SuggestedCourse).filter(
            SuggestedCourse.test_id == test_id
        ).all()
        
        return {
            "test": test,
            "questions": questions,
            "suggested_courses": [sc.course_name for sc in suggested_courses]
        }