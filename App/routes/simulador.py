from fastapi import APIRouter, Depends
from app.schemas import SimulationIn, SimulationOut
from app.services.ml_service import predict_bolsa
from app.db.session import get_db

router = APIRouter(prefix="/simulacoes")

@router.post("/", response_model=SimulationOut)
def create_simulation(payload: SimulationIn, user=Depends(get_current_user), db=Depends(get_db)):
# valida dados, salva entrada no DB
    result = predict_bolsa(payload.dict())
# salva resultado no DB
    return {"id": 123, "chance": result["chance"], "details": {}}
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/simulacoes", tags=["simulacoes"])
