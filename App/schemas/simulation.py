from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Schemas para simulações de ingresso
class SimulationCreate(BaseModel):
    ano_enem: int
    nota_redacao: float
    nota_natureza: float
    nota_humanas: float
    nota_linguagens: float
    nota_matematica: float
    estado: str
    modalidade: str

# Resultado da simulação
class SimulationResult(BaseModel):
    curso: str
    instituicao: str
    nota_usuario: float
    nota_corte: float
    chance_ingresso: float
    resultado: str

# Schema para resposta de simulação
class SimulationResponse(BaseModel):
    id_simulacao: int
    percentual_ingresso: float
    cursos_resultado: List[SimulationResult]

# Schema para histórico de simulações do usuário
class SimulationHistory(BaseModel):
    id: int
    ano_enem: int
    media_usuario: float
    estado: str
    modalidade: str
    created_at: datetime

    class Config:
        from_attributes = True