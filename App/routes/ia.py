from fastapi import APIRouter
from services.ia_service import IAService

router = APIRouter()
ia_service = IAService()

@router.post("/teste")
async def ia_test_endpoint(data: dict):
    answers = data.get("respostas", [])
    result = ia_service.predict_vocational_area(answers)
    
    return {
        "area_predita": result["area_predita"],
        "confianca": result["confianca"],
        "cursos_sugeridos": result["cursos_sugeridos"]
    }

@router.post("/result")
async def ia_result_endpoint(data: dict):
    # Endpoint para resultados finais do teste
    return {
        "area": "Ciências Humanas",
        "cursosSugeridos": ["Psicologia", "História", "Sociologia", "Jornalismo"]
    }

@router.post("/simulacao")
async def ia_simulation_endpoint(data: dict):
    user_data = {
        'nota_redacao': data.get('nota_redacao', 0),
        'nota_natureza': data.get('nota_natureza', 0),
        'nota_humanas': data.get('nota_humanas', 0),
        'nota_linguagens': data.get('nota_linguagens', 0),
        'nota_matematica': data.get('nota_matematica', 0)
    }
    
    result = ia_service.predict_scholarship_chance(user_data)
    return result

@router.post("/chat")
async def ia_chat_endpoint(data: dict):
    message = data.get("mensagem", "")
    context = data.get("contexto", {})
    
    response = ia_service.chat_response(message, context)
    return response