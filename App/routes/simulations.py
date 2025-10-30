from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from schemas.simulation import SimulationCreate
from services.simulation_service import SimulationService

router = APIRouter()

@router.post("/")
async def create_simulation(simulation_data: SimulationCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    simulation_service = SimulationService(db)
    
    # Calcular média
    notas = [
        simulation_data.nota_redacao,
        simulation_data.nota_natureza, 
        simulation_data.nota_humanas,
        simulation_data.nota_linguagens,
        simulation_data.nota_matematica
    ]
    media = sum(notas) / len(notas)
    
    # Criar simulação
    simulation = simulation_service.create_simulation(current_user["user_id"], simulation_data, media)
    
    # Buscar cursos compatíveis
    results = simulation_service.find_compatible_courses(simulation_data, media)
    
    return {
        "success": True,
        "data": {
            "id_simulacao": simulation.id,
            "percentual_ingresso": 72.34,
            "cursos_resultado": results
        }
    }

@router.get("/{simulation_id}")
async def get_simulation(simulation_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    simulation_service = SimulationService(db)
    
    simulation = simulation_service.get_simulation(simulation_id, current_user["user_id"])
    
    return {
        "success": True,
        "data": simulation
    }

@router.get("/historico")
async def get_simulation_history(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    simulation_service = SimulationService(db)
    
    simulations = simulation_service.get_user_simulations(current_user["user_id"])
    
    return {
        "success": True,
        "data": simulations
    }