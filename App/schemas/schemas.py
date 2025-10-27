from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool

class Config:
    orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TesteCreate(BaseModel):
    respostas: dict

class TesteOut(BaseModel):
    id: int
    user_id: int
    respostas: dict
    resultado: dict
    created_at: datetime

class Config:
    orm_mode = True

class SimulacaoCreate(BaseModel):
    nota_enem: float
    modalidade: str
    curso: str

class SimulacaoOut(BaseModel):
    id: int
    user_id: int
    nota_enem: float
    modalidade: str
    curso: str
    resultado: dict
    created_at: datetime

class Config:
    orm_mode = True

# Schemas para CRUD administrativo
class CursoCreate(BaseModel):
    nome: str
    area: Optional[str]
    orm_mode = True

class CursoOut(BaseModel):
    id: int
    nome: str
    area: Optional[str]
    instituicao: Optional[str]
    descricao: Optional[str]
    created_at: datetime

class Config:
    orm_mode = True

class BolsaCreate(BaseModel):
    curso_id: int
    tipo: str
    percentual: float
    descricao: Optional[str]

class BolsaOut(BaseModel):
    id: int
    curso_id: int
    tipo: str
    percentual: float
    descricao: Optional[str]
    created_at: datetime

class Config:
    orm_mode = True

class NotaCorteCreate(BaseModel):
    curso_id: int
    ano: int
    modalidade: str
    nota: float

class NotaCorteOut(BaseModel):
    id: int
    curso_id: int
    ano: int
    modalidade: str
    nota: float
    created_at: datetime

class Config:
    orm_mode = True 