from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from schemas.test import TestStart, TestAnswer, TestFinish
from services.test_service import TestService

router = APIRouter()

# Rota para iniciar um teste
@router.post("/start")
async def start_test(test_data: TestStart, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    test_service = TestService(db)
    
    test = test_service.start_test(current_user["user_id"], test_data)
    
    return {
        "success": True,
        "data": {
            "test_id": test.id,
            "test_name": test.test_name,
            "first_question": "Qual área mais te interessa?"
        }
    }

# Rota para responder uma pergunta do teste
@router.post("/answer")
async def answer_question(answer_data: TestAnswer, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    test_service = TestService(db)
    
    result = test_service.save_answer(answer_data)
    
    return {
        "success": True,
        "data": {
            "next_question": "Próxima pergunta...",
            "progress": "75%"
        }
    }

# Rota para finalizar o teste e obter resultados
@router.post("/finish")
async def finish_test(finish_data: TestFinish, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    test_service = TestService(db)
    
    result = test_service.finish_test(finish_data.test_id)
    
    return {
        "success": True,
        "data": {
            "area_conhecimento": result.area_conhecimento,
            "cursosSugeridos": [
                "Psicologia",
                "História", 
                "Sociologia",
                "Jornalismo"
            ]
        }
    }

# Rota para obter o histórico de testes do usuário
@router.get("/history")
async def get_test_history(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    test_service = TestService(db)
    
    tests = test_service.get_user_tests(current_user["user_id"])
    
    return {
        "success": True,
        "data": tests
    }