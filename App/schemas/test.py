from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TestStart(BaseModel):
    nome_teste: str
    modo: str = "gratuito"

class TestAnswer(BaseModel):
    test_id: int
    pergunta_id: int
    resposta: str

class TestFinish(BaseModel):
    test_id: int

class TestResponse(BaseModel):
    area: str
    cursosSugeridos: List[str]

class TestHistory(BaseModel):
    id: int
    test_name: str
    status: str
    area_conhecimento: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True