from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SimulationCreate(BaseModel):
    ano_enem: int
    nota_redacao: float
    nota_natureza: float
    nota_humanas: float
    nota_linguagens: float
    nota_matematica: float
    estado: str
    modalidade: str

class SimulationResult(BaseModel):
    curso: str
    instituicao: str
    nota_usuario: float
    nota_corte: float
    chance_ingresso: float
    resultado: str

class SimulationResponse(BaseModel):
    id_simulacao: int
    percentual_ingresso: float
    cursos_resultado: List[SimulationResult]

class SimulationHistory(BaseModel):
    id: int
    ano_enem: int
    media_usuario: float
    estado: str
    modalidade: str
    created_at: datetime

    class Config:
        from_attributes = True