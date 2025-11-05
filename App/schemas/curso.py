from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schemas para cursos e notas de corte
class CourseBase(BaseModel):
    nome: str
    area: str
    instituicao: str
    estado: str
    duracao_anos: int
    valor: float

#  Schema para criação de curso
class CourseCreate(CourseBase):
    pass

# Schema para resposta de curso
class CourseResponse(CourseBase):
    id: int
    tipo_instituicao: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Schema para nota de corte
class CutoffUpdate(BaseModel):
    nome_instituicao: str
    nome_curso: str
    estado: str
    modalidade: str
    ano: int
    nova_nota_corte: float

# Schema para criação de bolsa
class ScholarshipCreate(BaseModel):
    programa: str
    percentual_desconto: int