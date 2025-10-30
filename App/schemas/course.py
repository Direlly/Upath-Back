from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CourseBase(BaseModel):
    nome: str
    area: str
    instituicao: str
    estado: str
    duracao_anos: int
    valor: float

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    tipo_instituicao: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class CutoffUpdate(BaseModel):
    nome_instituicao: str
    nome_curso: str
    estado: str
    modalidade: str
    ano: int
    nova_nota_corte: float

class ScholarshipCreate(BaseModel):
    programa: str
    percentual_desconto: int