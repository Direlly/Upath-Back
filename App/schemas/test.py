from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schemas para testes de perfil vocacional
class TestStart(BaseModel):
    nome_teste: str
    modo: str = "gratuito"

# Resposta do teste
class TestAnswer(BaseModel):
    test_id: int
    pergunta_id: int
    resposta: str

# Finalização do teste
class TestFinish(BaseModel):
    test_id: int

# Schema para resposta do teste
class TestResponse(BaseModel):
    area: str
    cursosSugeridos: List[str]

# Schema para histórico de testes do usuário
class TestHistory(BaseModel):
    id: int
    test_name: str
    status: str
    area_conhecimento: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True